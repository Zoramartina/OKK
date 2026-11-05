#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPTV 直播源自动清洗

读取 source/ 下的 txt / m3u 源文件，逐条探测可用性，输出分类整理的播放列表到 dist/。

    python scripts/clean.py                  # 按 config.json 跑全量
    python scripts/clean.py --limit 20       # 只测前 20 条，调试用
    python scripts/clean.py --mode loose     # 只验连通性，不测分片速度

校验结果是三态，不是二态：
    verified   真跑通了（拉到 m3u8 且分片有数据）
    unverified 保留但没验成（IPv6 源在 Actions 上必然如此、加密流、探测超时但历史有效）
    dead       明确失效，删除
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urljoin, urlparse

# ---------------------------------------------------------------- 常量

ATTR_RE = re.compile(r'([A-Za-z0-9_-]+)="([^"]*)"')
RES_RE = re.compile(r'RESOLUTION=(\d+)x(\d+)')
BANDWIDTH_RE = re.compile(r'(?:AVERAGE-)?BANDWIDTH=(\d+)')
SCHEME_RE = re.compile(r'^[A-Za-z][A-Za-z0-9+.\-]*://')

IS_CI = __import__("os").environ.get("GITHUB_ACTIONS") == "true"

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

_DNS_CACHE: dict[str, str] = {}

DEFAULTS = {
    "inputs": ["source"],
    "remote": [],
    "output_dir": "dist",
    "primary_output": "",
    "group_headers": True,
    "concurrency": 64,
    "per_host": 6,
    "timeout": 6,
    "probe_seconds": 4,
    "dns_timeout": 5,
    "mode": "strict",
    "probe_bytes": 262144,
    "retries": 1,
    "keep_ipv6": True,
    "max_per_channel": 5,
    "min_kbps": 0,
    "epg_url": "",
    "user_agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "categories": [
        {"file": "cctv.m3u", "match": ["CCTV", "央视", "CGTN"]},
        {"file": "weishi.m3u", "match": ["卫视"]},
        {"file": "difang.m3u", "match": ["地方", "城市", "省内", "影视", "体育", "少儿"]},
    ],
}


# ---------------------------------------------------------------- 数据结构


@dataclass
class Entry:
    name: str
    url: str
    group: str = ""
    tvg_id: str = ""
    tvg_logo: str = ""
    src: str = ""
    attrs: dict = field(default_factory=dict)   # 原始 EXTINF 的全部属性，原样回写
    origin: str = "local"                       # local = source/ 里的主源；remote = 自动搜集

    state: str = "pending"      # verified | unverified | dead
    code: int = 0
    ms: int = 0
    kbps: float = 0.0
    res: str = ""
    note: str = ""

    @property
    def ok(self) -> bool:
        return self.state in ("verified", "unverified")

    @property
    def ua(self) -> str:
        return (self.attrs.get("http-user-agent") or "").strip()

    @property
    def referer(self) -> str:
        ref = (self.attrs.get("http-referer") or "").strip()
        if ref:
            return ref
        hdr = (self.attrs.get("http-header") or "").strip()
        for part in hdr.split("&"):
            k, _, v = part.partition("=")
            if k.strip().lower() == "referer":
                return v.strip()
        return ""

    @property
    def sort_key(self):
        # 验证过的排前面，同频道按速度降序
        return (self.state != "verified", self.group, self.name, -self.kbps)


# ---------------------------------------------------------------- 解析输入


def parse_m3u(text: str, src: str, origin: str = "local") -> Iterable[Entry]:
    pending = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.upper().startswith("#EXTINF"):
            head, _, tail = line.partition(",")
            attrs = dict(ATTR_RE.findall(head))
            name = tail.strip() or attrs.get("tvg-name", "").strip()
            pending = (name, attrs)
        elif line.startswith("#"):
            continue
        elif pending is not None:
            name, attrs = pending
            if SCHEME_RE.match(line):
                yield Entry(
                    name=name,
                    url=line,
                    group=attrs.get("group-title", "").strip(),
                    tvg_id=attrs.get("tvg-id", "").strip(),
                    tvg_logo=attrs.get("tvg-logo", "").strip(),
                    src=src,
                    attrs=attrs,
                    origin=origin,
                )
            pending = None


def parse_txt(text: str, src: str, origin: str = "local") -> Iterable[Entry]:
    group = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        if "#genre#" in line:
            group = line.split(",")[0].replace("#genre#", "").strip()
            continue
        for sep in (",", "|", "，", "｜"):
            if sep in line:
                name, rest = line.split(sep, 1)
                break
        else:
            continue
        name = name.strip()
        for url in rest.split("#"):
            url = url.strip()
            if SCHEME_RE.match(url):
                yield Entry(name=name, url=url, group=group, src=src, origin=origin)


def load_entries(inputs: list[str], root: Path) -> list[Entry]:
    entries: list[Entry] = []
    for item in inputs:
        p = (root / item).resolve()
        if p.is_file():
            files = [p]
        elif p.is_dir():
            files = sorted(
                f for f in p.rglob("*")
                if f.suffix.lower() in (".txt", ".m3u", ".m3u8") and f.is_file()
            )
        else:
            print(f"  [warn] 输入不存在，跳过: {item}")
            continue

        for f in files:
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError as e:
                print(f"  [warn] 读不了 {f.name}: {e}")
                continue
            if f.suffix.lower() == ".txt":
                got = list(parse_txt(text, f.name, "local"))
            else:
                got = list(parse_m3u(text, f.name, "local"))
            print(f"  {f.name:<24} {len(got):>5} 条")
            entries.extend(got)
    return entries


def load_remote(urls: list[str], cfg: dict) -> list[Entry]:
    """从远程地址拉取源。地址可以是 raw 原文，也可以是 gh-proxy 之类的镜像地址。"""
    entries: list[Entry] = []
    for url in urls:
        try:
            with _open(url, cfg, max(cfg["timeout"], 15)) as resp:
                raw, _ = _read_capped(resp, 8 * 1024 * 1024, 60)
            text = raw.decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"  [warn] 远程拉取失败 {url[:60]}: {type(e).__name__}")
            continue
        if text.lstrip().startswith("#EXTM3U"):
            got = list(parse_m3u(text, url, "remote"))
        else:
            got = list(parse_txt(text, url, "remote"))
        label = url.rsplit("/", 1)[-1][:24]
        print(f"  {label:<24} {len(got):>5} 条")
        entries.extend(got)
    return entries


def dedupe(entries: list[Entry]) -> list[Entry]:
    seen: set[str] = set()
    out: list[Entry] = []
    for e in entries:
        key = re.sub(r"^(https?)://", "", e.url.strip().lower())
        key = key.rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        e.name = re.sub(r"\s+", " ", e.name).strip()
        if not e.name:
            e.name = "未命名"
        out.append(e)
    return out


# ---------------------------------------------------------------- 网络探测


def host_stack(url: str) -> str:
    """判断目标地址的 IP 栈：v6only / v4。只在 CI 里调用，避免本地多花时间。"""
    host = urlparse(url).hostname
    if not host:
        return "v4"
    if host in _DNS_CACHE:
        return _DNS_CACHE[host]

    result = "v4"
    try:
        ipaddress.IPv6Address(host.strip("[]"))
        result = "v6only"
    except ValueError:
        try:
            infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
            families = {i[0] for i in infos}
            if families == {socket.AF_INET6}:
                result = "v6only"
        except (socket.gaierror, OSError):
            result = "v4"
    _DNS_CACHE[host] = result
    return result


SAFE_CHARS = ":/?#[]@!$&'()*+,;=%~"


def _open(url: str, cfg: dict, timeout: float, ua: str | None = None, referer: str | None = None):
    # 源里常见 ?id=湖南卫视 这种中文查询串，urllib 不接受非 ASCII，必须先转义
    url = quote(url, safe=SAFE_CHARS)
    headers = {
        "User-Agent": ua or cfg["user_agent"],
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "Connection": "close",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX)


def _read_capped(resp, max_bytes: int, seconds: float) -> tuple[bytes, float]:
    buf = bytearray()
    t0 = time.perf_counter()
    while len(buf) < max_bytes:
        chunk = resp.read(16384)
        if not chunk:
            break
        buf.extend(chunk)
        if time.perf_counter() - t0 > seconds:
            break
    return bytes(buf), time.perf_counter() - t0


def _pick_variant(body: str) -> str | None:
    """从 master playlist 里挑码率/分辨率最高的一路。"""
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    best, best_score = None, -1
    for i, line in enumerate(lines):
        if not line.upper().startswith("#EXT-X-STREAM-INF"):
            continue
        if i + 1 >= len(lines) or lines[i + 1].startswith("#"):
            continue
        score = 0
        m = RES_RE.search(line)
        if m:
            score = int(m.group(1)) * int(m.group(2))
        else:
            b = BANDWIDTH_RE.search(line)
            if b:
                score = int(b.group(1)) // 100
        if score > best_score:
            best, best_score = lines[i + 1], score
    return best


def _abs_url(base: str, ref: str) -> str:
    return urljoin(base, ref)


def _level_label(res: str) -> str:
    if not res:
        return ""
    w, _, h = res.partition("x")
    try:
        hh = int(h)
    except ValueError:
        return ""
    if hh >= 2160:
        return "4K"
    if hh >= 1080:
        return "1080P"
    if hh >= 720:
        return "720P"
    if hh >= 576:
        return "576P"
    if hh >= 480:
        return "480P"
    return "SD"


def _note_for(e: Exception) -> str:
    reason = getattr(e, "reason", e)
    s = f"{reason}".lower()
    if "ssl" in s or "handshake" in s:
        return "TLS 握手失败"
    if "timed out" in s or isinstance(reason, TimeoutError):
        return "连接超时"
    if "refused" in s or "10061" in s:
        return "连接被拒"
    if "getaddrinfo" in s or "name or service" in s:
        return "域名解析失败"
    if "reset" in s or "10054" in s:
        return "连接被重置"
    return type(e).__name__


_HOST_SEMS: dict[str, threading.Semaphore] = {}
_HOST_LOCK = threading.Lock()


def _host_slot(netloc: str, limit: int) -> threading.Semaphore:
    """同一个宿主下的频道可能有几十条，全放出去等于自己把自己打成 403。"""
    with _HOST_LOCK:
        sem = _HOST_SEMS.get(netloc)
        if sem is None:
            sem = threading.Semaphore(max(1, limit))
            _HOST_SEMS[netloc] = sem
        return sem


def probe(entry: Entry, cfg: dict) -> Entry:
    netloc = urlparse(entry.url).netloc if SCHEME_RE.match(entry.url) else ""
    if not netloc:
        return _probe(entry, cfg)
    with _host_slot(netloc, int(cfg.get("per_host", 6))):
        return _probe(entry, cfg)


def _probe(entry: Entry, cfg: dict) -> Entry:
    if not entry.url.startswith(("http://", "https://")):
        entry.state = "unverified"
        entry.note = f"非 http(s) 协议（{entry.url.split(':')[0]}）"
        return entry

    ua, ref = entry.ua or None, entry.referer or None

    if IS_CI and cfg["keep_ipv6"] and host_stack(entry.url) == "v6only":
        entry.state = "unverified"
        entry.note = "IPv6 源，Actions 无 IPv6 无法校验"
        return entry

    t0 = time.perf_counter()
    final_url = entry.url
    try:
        with _open(entry.url, cfg, cfg["timeout"], ua, ref) as resp:
            entry.code = resp.status
            head, _ = _read_capped(resp, 8192, 2)
            final_url = resp.geturl()
            ctype = (resp.headers.get("Content-Type") or "").lower()
    except urllib.error.HTTPError as e:
        entry.code = e.code
        entry.ms = int((time.perf_counter() - t0) * 1000)
        if e.code in (403, 429):
            # 大面积 403 多半是自己打太狠被限流，也可能是地区限制或反盗链。
            # 这类不能判死，留着等第二轮冷却复测。
            entry.state = "unverified"
            entry.note = f"HTTP {e.code}（限流/地区限制）"
        else:
            entry.state = "dead"
            entry.note = f"HTTP {e.code}"
        return entry
    except Exception as e:
        entry.state, entry.ms = "dead", int((time.perf_counter() - t0) * 1000)
        entry.note = _note_for(e)
        return entry

    is_playlist = head.lstrip().startswith(b"#EXTM3U") or "mpegurl" in ctype
    if not is_playlist:
        if head[:1] in (b"\x47", b"\x00") or "mp2t" in ctype or "video/" in ctype:
            entry.state, entry.ms = "verified", int((time.perf_counter() - t0) * 1000)
            entry.note = "直连流"
            return entry
        entry.state, entry.ms = "dead", int((time.perf_counter() - t0) * 1000)
        entry.note = "返回非流内容"
        return entry

    if cfg["mode"] != "strict":
        entry.state, entry.ms = "verified", int((time.perf_counter() - t0) * 1000)
        entry.note = "loose"
        return entry

    # ---- strict: 往下追一层，真下一段分片
    try:
        with _open(final_url, cfg, cfg["timeout"], ua, ref) as resp:
            body, _ = _read_capped(resp, 65536, cfg["probe_seconds"])
        text = body.decode("utf-8", errors="ignore")

        if "#EXT-X-KEY" in text and "METHOD=NONE" not in text:
            entry.state = "verified"
            entry.ms = int((time.perf_counter() - t0) * 1000)
            entry.note = "加密流（未验分片）"
            return entry

        media_url = final_url
        variant = _pick_variant(text)
        if variant:
            media_url = _abs_url(final_url, variant)
            with _open(media_url, cfg, cfg["timeout"], ua, ref) as resp:
                vbody, _ = _read_capped(resp, 65536, cfg["probe_seconds"])
            text = vbody.decode("utf-8", errors="ignore")

        seg = ""
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            seg = line
            break
        if not seg:
            entry.state, entry.ms = "dead", int((time.perf_counter() - t0) * 1000)
            entry.note = "播放列表为空"
            return entry

        seg_url = _abs_url(media_url, seg)
        with _open(seg_url, cfg, min(cfg["timeout"], cfg["probe_seconds"] + 3), ua, ref) as resp:
            data, elapsed = _read_capped(resp, cfg["probe_bytes"], cfg["probe_seconds"])

        if not data:
            entry.state, entry.ms = "dead", int((time.perf_counter() - t0) * 1000)
            entry.note = "分片无数据"
            return entry

        # 采样窗口太短时算出来的速度会虚高几十倍，宁可留空也不写假数据
        if elapsed >= 0.25 and len(data) >= 65536:
            entry.kbps = round(min(len(data) * 8 / 1000 / elapsed, 200000), 1)
        else:
            entry.kbps = 0.0
        entry.ms = int((time.perf_counter() - t0) * 1000)
        entry.state = "verified"

        m = RES_RE.search(text)
        entry.res = _level_label(f"{m.group(1)}x{m.group(2)}") if m else ""
        return entry

    except Exception as e:
        entry.ms = int((time.perf_counter() - t0) * 1000)
        if cfg["mode"] == "strict" and entry.code == 200:
            # 列表能拉到但分片追不下去，多半是反盗链，保留但降级
            entry.state = "unverified"
            entry.note = f"分片探测失败: {type(e).__name__}"
        else:
            entry.state, entry.note = "dead", f"{type(e).__name__}"
        return entry


def _resolve(host: str, timeout: float):
    """带超时的域名解析。socket.getaddrinfo 本身没有超时参数，
    一个死域名能把整个任务拖住几十秒，只能丢到 daemon 线程里等。"""
    box: dict = {}

    def run():
        try:
            box["r"] = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        except Exception:
            box["r"] = None

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout)
    return box.get("r")


def preflight_dns(entries: list[Entry], cfg: dict) -> None:
    hosts = set()
    for e in entries:
        if e.url.startswith(("http://", "https://")):
            h = urlparse(e.url).hostname
            if h:
                hosts.add(h)
    if not hosts:
        return

    print(f"  预解析 {len(hosts)} 个域名（单域名超时 {cfg['dns_timeout']}s）")
    results: dict[str, bool] = {}
    threads = []
    for h in hosts:
        t = threading.Thread(target=lambda x=h: results.__setitem__(x, bool(_resolve(x, cfg["dns_timeout"]))), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    bad = {h for h, ok in results.items() if not ok}
    if bad:
        hit = 0
        for e in entries:
            if urlparse(e.url).hostname in bad:
                e.state = "unverified"
                e.note = "域名解析失败"
                hit += 1
        print(f"  {len(bad)} 个域名解析失败，{hit} 条转为保留未校验（不判死，可能是本地 DNS 问题）")


def run_probes(entries: list[Entry], cfg: dict) -> None:
    preflight_dns(entries, cfg)

    todo = [e for e in entries if e.state == "pending"]
    total = len(todo)
    done = 0
    t0 = time.perf_counter()
    step = max(1, total // 10)

    def work(e: Entry) -> Entry:
        return probe(e, cfg)

    with ThreadPoolExecutor(max_workers=cfg["concurrency"]) as pool:
        futures = [pool.submit(work, e) for e in todo]
        for fut in futures:
            fut.result()
            done += 1
            if done % step == 0 or done == total:
                print(f"  进度 {done}/{total}", flush=True)

    # 第二轮：只重试第一轮因为网络抖动失败的，降低偶发超时造成的误杀
    retries = int(cfg.get("retries", 0))
    for r in range(retries):
        dead = [e for e in entries if e.state == "dead" and e.note != "域名解析失败"]
        if not dead:
            break
        print(f"  重试第 {r + 1} 轮，{len(dead)} 条")
        with ThreadPoolExecutor(max_workers=cfg["concurrency"]) as pool:
            list(pool.map(work, dead))

    # 403/429 不做批量复测。实测冷却 6 秒后复测一条都救不回来，
    # 真正的恢复窗口是几分钟级，批量重打只会再次触发限流。
    # 这类源统一按「保留未校验」处理，不删除。

    print(f"  探测用时 {time.perf_counter() - t0:.1f}s")


# ---------------------------------------------------------------- 输出


def fmt_speed(kbps: float) -> str:
    return f"{kbps / 1000:.1f}M" if kbps >= 1000 else f"{int(kbps)}K"


def write_m3u(path: Path, entries: list[Entry], cfg: dict, with_status: bool = False) -> None:
    lines = []
    head = "#EXTM3U"
    if cfg.get("epg_url"):
        head += f' x-tvg-url="{cfg["epg_url"]}"'
    lines.append(head)

    last_group = None
    for e in entries:
        # 沿用原文件用 "#分组名" 当分隔符的写法
        if cfg.get("group_headers") and e.group and e.group != last_group:
            lines.append("")
            lines.append(f"#{e.group}")
            last_group = e.group

        attrs = dict(e.attrs or {})
        if e.tvg_id:
            attrs["tvg-id"] = e.tvg_id
        if e.tvg_logo:
            attrs["tvg-logo"] = e.tvg_logo
        if e.group:
            attrs["group-title"] = e.group
        attrs.setdefault("tvg-name", e.name)
        if with_status:
            bits = [b for b in (e.res, fmt_speed(e.kbps) if e.kbps else "") if b]
            if e.state == "unverified" and e.note:
                bits.append(e.note)
            if bits:
                attrs["tvg-name"] = f"{e.name} [{'.'.join(bits)}]"

        order = ["tvg-id", "tvg-name", "tvg-logo", "group-title"]
        ordered = [(k, attrs[k]) for k in order if attrs.get(k)]
        ordered += [(k, v) for k, v in attrs.items() if k not in order and v]
        attr_str = " ".join(f'{k}="{v}"' for k, v in ordered if '"' not in str(v))

        display = attrs["tvg-name"] if with_status else e.name
        lines.append(f"#EXTINF:-1 {attr_str},{display}")
        lines.append(e.url)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(path: Path, entries: list[Entry], cfg: dict) -> None:
    verified = [e for e in entries if e.state == "verified"]
    unverified = [e for e in entries if e.state == "unverified"]
    dead = [e for e in entries if e.state == "dead"]

    names = {e.name for e in entries if e.ok}
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M (UTC+8)")

    out = [
        "# 直播源清洗报告",
        "",
        f"生成时间：{now}",
        "",
        "| 指标 | 数值 |",
        "| --- | --- |",
        f"| 原始条目 | {len(entries)} |",
        f"| 已验证可播 | {len(verified)} |",
        f"| 保留未校验 | {len(unverified)} |",
        f"| 已剔除 | {len(dead)} |",
        f"| 有效频道数 | {len(names)} |",
    ]
    if verified:
        avg = sum(e.ms for e in verified) / len(verified)
        out.append(f"| 平均响应 | {avg:.0f} ms |")

    if unverified:
        out += ["", "## 保留但未校验", "", "| 频道 | 原因 |", "| --- | --- |"]
        for e in unverified[:30]:
            out.append(f"| {e.name} | {e.note} |")

    if dead:
        out += ["", "## 已剔除", "", "| 频道 | 状态 | 地址 |", "| --- | --- | --- |"]
        for e in dead[:60]:
            out.append(f"| {e.name} | {e.note} | `{e.url[:70]}` |")
        if len(dead) > 60:
            out.append(f"| … | 另有 {len(dead) - 60} 条 | |")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def write_detail(path: Path, entries: list[Entry]) -> None:
    """逐条明细，方便自己翻哪些死了、为什么死。"""
    rows = ["状态\t频道\t分组\t响应ms\t速度kbps\t备注\t地址"]
    for e in sorted(entries, key=lambda x: (x.state, x.group, x.name)):
        rows.append("\t".join([e.state, e.name, e.group, str(e.ms), str(e.kbps), e.note, e.url]))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def apply_limit_per_channel(entries: list[Entry], limit: int) -> list[Entry]:
    """只对自动搜集来的源做条数限制。主源里手工挑选的线路全部保留，
    因为那些多线路是刻意留的备份，砍掉等于破坏人工成果。"""
    if limit <= 0:
        return entries
    counter: dict[str, int] = {}
    out = []
    for e in entries:
        if not e.ok:
            continue
        if e.origin != "remote":
            out.append(e)
            continue
        key = e.name.lower()
        if counter.get(key, 0) >= limit:
            continue
        counter[key] = counter.get(key, 0) + 1
        out.append(e)
    return out


# ---------------------------------------------------------------- 主流程


def load_config(path: Path) -> dict:
    cfg = dict(DEFAULTS)
    if path.is_file():
        user = json.loads(path.read_text(encoding="utf-8"))
        cfg.update({k: v for k, v in user.items() if not k.startswith("_")})
    return cfg


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    ap = argparse.ArgumentParser(description="IPTV 直播源自动清洗")
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--input", action="append", help="覆盖 config 里的 inputs，可多次指定")
    ap.add_argument("--remote", action="append", help="追加远程源地址，可多次指定")
    ap.add_argument("--out", default=None, help="覆盖输出目录")
    ap.add_argument("--mode", choices=["strict", "loose"], default=None)
    ap.add_argument("--concurrency", type=int, default=None)
    ap.add_argument("--timeout", type=float, default=None)
    ap.add_argument("--limit", type=int, default=0, help="只测前 N 条，调试用")
    args = ap.parse_args()

    root = Path.cwd()
    cfg = load_config(root / args.config)
    if args.input:
        cfg["inputs"] = args.input
    if args.remote:
        cfg["remote"] = list(cfg.get("remote") or []) + args.remote
    if args.out:
        cfg["output_dir"] = args.out
    if args.mode:
        cfg["mode"] = args.mode
    if args.concurrency:
        cfg["concurrency"] = args.concurrency
    if args.timeout:
        cfg["timeout"] = args.timeout

    print(f"模式 {'GitHub Actions（境外 IP，无 IPv6）' if IS_CI else '本地'}"
          f"　校验 {cfg['mode']}　并发 {cfg['concurrency']}")

    print("\n[1/4] 读取源文件")
    entries = load_entries(cfg["inputs"], root)
    if cfg.get("remote"):
        print(f"  远程源 {len(cfg['remote'])} 个")
        entries += load_remote(cfg["remote"], cfg)
    entries = dedupe(entries)
    if not entries:
        print("没有读到任何条目，检查 source/ 目录")
        return 1
    if args.limit:
        entries = entries[: args.limit]
    print(f"  去重后 {len(entries)} 条")

    print("\n[2/4] 探测可用性")
    run_probes(entries, cfg)

    print("\n[3/4] 整理输出")
    good = sorted([e for e in entries if e.ok], key=lambda e: e.sort_key)
    good = apply_limit_per_channel(good, int(cfg.get("max_per_channel", 0)))

    out_dir = root / cfg["output_dir"]
    write_m3u(out_dir / "all.m3u", good, cfg)
    write_m3u(out_dir / "all_status.m3u", good, cfg, with_status=True)

    # 主订阅：只含 source/ 里手工挑选的源，保持原文件名不变，订阅地址不受影响
    local = [e for e in good if e.origin == "local"]
    if cfg.get("primary_output") and local:
        write_m3u(root / cfg["primary_output"], local, cfg)
        print(f"  主订阅 {cfg['primary_output']}：{len(local)} 条")

    groups = sorted({e.group for e in good if e.group})
    if cfg.get("group_files", True):
        for g in groups:
            sub = [e for e in good if e.group == g]
            safe = re.sub(r'[\\/:*?"<>|\s]+', "_", g)[:40]
            write_m3u(out_dir / "groups" / f"{safe}.m3u", sub, cfg)

    matched: set[str] = set()
    for cat in cfg.get("categories", []):
        keys = [k.lower() for k in cat.get("match", [])]
        sub = [e for e in good if any(k in (e.group + " " + e.name).lower() for k in keys)]
        if sub:
            write_m3u(out_dir / cat["file"], sub, cfg)
            matched.update(e.url for e in sub)
    rest = [e for e in good if e.url not in matched]
    if rest:
        write_m3u(out_dir / "other.m3u", rest, cfg)

    write_report(out_dir / "report.md", entries, cfg)
    write_detail(out_dir / "detail.tsv", entries)

    print("\n[4/4] 完成")
    v = sum(1 for e in entries if e.state == "verified")
    u = sum(1 for e in entries if e.state == "unverified")
    d = sum(1 for e in entries if e.state == "dead")
    print(f"  已验证 {v}　保留未校验 {u}　剔除 {d}　输出 {len(good)} 条")
    print(f"  → {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
