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
    "liveness_gap": 90,
    "keep_ipv6": True,
    "max_per_channel": 5,
    "min_kbps": 0,
    "epg_url": "",
    # 只把「实测通过」的源写进订阅，其余一律剔除。
    # CI 上默认关闭：Actions 是境外 IP，会把只允许大陆访问的源整批误删。
    "drop_unverified": True,
    "drop_unverified_in_ci": False,
    # 403/429 半数其实是高并发限流误判，整轮结束后冷却再低速复核。
    "soft_recheck_rounds": 2,
    "soft_recheck_workers": 6,
    "soft_recheck_cool": 20,
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
    seq: int = -1               # 播放列表媒体序列号，用于判断是否还在前进
    seg: str = ""               # 最后一个分片名，同上
    media_url: str = ""         # 真正承载分片列表的地址（master 会往下解析一层）
    checked_at: float = 0.0

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


def _capture(entry: Entry, url: str, body: bytes) -> None:
    """记下播放列表指纹，供稍后的活性复检比对。master 列表没有分片，跳过。"""
    text = body.decode("utf-8", errors="ignore")
    if "#EXT-X-STREAM-INF" in text:
        return
    segs = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
    if not segs:
        return
    mseq = re.search(r"#EXT-X-MEDIA-SEQUENCE:(\d+)", text)
    entry.media_url = url
    entry.seq = int(mseq.group(1)) if mseq else -1
    entry.seg = segs[-1].rsplit("/", 1)[-1]
    entry.checked_at = time.time()


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
            # 一次读全列表，strict 阶段直接用，不重复请求一遍
            head, _ = _read_capped(resp, 65536, 2)
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
        _capture(entry, final_url, head)
        return entry

    # ---- strict: 往下追一层，真下一段分片
    try:
        # 上面那次请求已经把列表读全了，直接复用，省掉一次往返
        body = head
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

        segs = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
        if not segs:
            entry.state, entry.ms = "dead", int((time.perf_counter() - t0) * 1000)
            entry.note = "播放列表为空"
            return entry

        # 记下序列号和末尾分片，稍后用来判断这张列表是不是冻住的
        entry.media_url = media_url
        mseq = re.search(r"#EXT-X-MEDIA-SEQUENCE:(\d+)", text)
        entry.seq = int(mseq.group(1)) if mseq else -1
        entry.seg = segs[-1].rsplit("/", 1)[-1]
        entry.checked_at = time.time()

        seg_url = _abs_url(media_url, segs[0])
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


def verify_liveness(entries: list[Entry], cfg: dict) -> None:
    """分片能下载，不代表是活直播。播放列表冻住的话，播放器会把最后几十秒
    画面无限循环——这就是「一直重复播放以前的内容」的成因。隔一段时间再抓一次，
    序列号没前进、末尾分片也没变，判定为停滞。"""
    gap = float(cfg.get("liveness_gap", 90))
    cand = [e for e in entries
            if e.state == "verified" and e.seq >= 0 and e.media_url
            and time.time() - e.checked_at >= gap]
    if not cand:
        return

    print(f"  活性复检 {len(cand)} 条（距首次探测已 ≥{gap:.0f}s）")

    def work(e: Entry):
        try:
            with _open(e.media_url, cfg, cfg["timeout"], e.ua or None, e.referer or None) as resp:
                body, _ = _read_capped(resp, 65536, cfg["probe_seconds"])
        except Exception:
            return
        text = body.decode("utf-8", errors="ignore")
        if "#EXT-X-ENDLIST" in text:
            e.state = "unverified"
            e.note = "点播列表（非直播）"
            return
        segs = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
        mseq = re.search(r"#EXT-X-MEDIA-SEQUENCE:(\d+)", text)
        seq = int(mseq.group(1)) if mseq else -1
        last = segs[-1].rsplit("/", 1)[-1] if segs else ""
        if seq == e.seq and last == e.seg:
            e.state = "unverified"
            e.note = "播放列表停滞（循环回放）"

    bs = max(1, int(cfg.get("batch_size", 0) or 0) or 100)
    bp = max(0.0, float(cfg.get("batch_pause", 0) or 0))
    for i in range(0, len(cand), bs):
        with ThreadPoolExecutor(max_workers=int(cfg["concurrency"])) as pool:
            list(pool.map(work, cand[i:i + bs]))
        if bp and i + bs < len(cand):
            time.sleep(bp)
    stale = sum(1 for e in cand if e.state == "unverified")
    print(f"  其中停滞/点播 {stale} 条")


def recheck_soft(entries: list[Entry], cfg: dict) -> None:
    """403/429 这类软失败，高并发下约一半是限流误判：取 16 个不同宿主串行复查，
    7 个能通、9 个真死。整轮结束后冷却，用条目自带的 UA/Referer 低速复核，
    能通就转正，多轮都不通才真正删除。换成浏览器 UA 反而更差（2/14 通，
    自带 UA 是 7/14），所以这里绝不能改 UA。
    复核只验连通性和 m3u8 头，不追分片，否则两千条要跑半小时。"""
    rounds = int(cfg.get("soft_recheck_rounds", 2))
    workers = max(1, int(cfg.get("soft_recheck_workers", 6)))
    cool = float(cfg.get("soft_recheck_cool", 20))
    if rounds <= 0:
        return

    def is_soft(e: Entry) -> bool:
        if e.state != "unverified":
            return False
        return (e.code in (403, 408, 429)
                or e.note in ("域名解析失败", "TimeoutError", "连接被重置")
                or e.note.startswith("分片探测失败"))

    # 信号量按宿主缓存，首轮是 per_host=4，复核要压到 1，先清掉旧的那批
    with _HOST_LOCK:
        _HOST_SEMS.clear()
    loose = dict(cfg)
    loose["mode"] = "loose"
    loose["per_host"] = 1
    loose["concurrency"] = workers

    for r in range(rounds):
        cand = [e for e in entries if is_soft(e)]
        if not cand:
            break
        wait = cool * (r + 1)
        print(f"  低速复核 {r + 1}/{rounds}：{len(cand)} 条，冷却 {wait:.0f}s 后并发 {workers}", flush=True)
        time.sleep(wait)

        def work(e: Entry) -> Entry:
            e.state, e.code, e.note = "pending", 0, ""
            return probe(e, loose)

        bs = max(1, int(cfg.get("batch_size", 0) or 0) or 100)
        bp = max(0.0, float(cfg.get("batch_pause", 0) or 0))
        for i in range(0, len(cand), bs):
            with ThreadPoolExecutor(max_workers=workers) as pool:
                list(pool.map(work, cand[i:i + bs]))
            if bp and i + bs < len(cand):
                time.sleep(bp)
        back = sum(1 for e in cand if e.state == "verified")
        print(f"    复核通过 {back} 条", flush=True)
        for e in cand:
            if e.state == "verified":
                e.note = "低速复核通过"

    still = [e for e in entries if is_soft(e)]
    for e in still:
        e.note = f"复核仍失败（{e.note}）"
        e.state = "dead"
    if still:
        print(f"  多轮复核仍失败 {len(still)} 条，判为失效", flush=True)


def load_state(path: Path) -> dict[str, tuple[str, str]]:
    """读上一轮的 detail.tsv，恢复每条的判定，供补核模式使用。"""
    if not path.exists():
        return {}
    out: dict[str, tuple[str, str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        cols = line.split("\t")
        if len(cols) >= 7:
            out[cols[6]] = (cols[0], cols[5])
    return out


def recheck_slow(entries: list[Entry], cfg: dict) -> None:
    """连续扫完几千条后，出口 IP 会进入限流状态，之后所有请求都是 403，
    秒级冷却救不回来，恢复窗口是分钟级。等网络空闲后，用极低速率把失败
    队列单独再过一遍，这一轮的结论才可信。"""
    cand = [e for e in entries if e.state != "verified"
            and e.url.startswith(("http://", "https://"))]
    if not cand:
        return
    slow = dict(cfg)
    slow["mode"] = "loose"
    slow["per_host"] = 1
    size = max(1, int(cfg.get("recheck_batch", 25)))
    pause = max(0.0, float(cfg.get("recheck_pause", 8)))
    workers = max(1, int(cfg.get("recheck_workers", 2)))
    with _HOST_LOCK:
        _HOST_SEMS.clear()
    print(f"  低速补核 {len(cand)} 条：并发 {workers}，每批 {size}，批间 {pause:.0f}s", flush=True)
    t0 = time.perf_counter()
    for i in range(0, len(cand), size):
        chunk = cand[i:i + size]

        def work(e: Entry) -> Entry:
            e.state, e.code, e.note = "pending", 0, ""
            e.seq, e.seg, e.media_url = -1, "", ""
            return probe(e, slow)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(work, chunk))
        for e in chunk:
            if e.state == "verified":
                e.note = "低速复核通过"
            elif e.state == "unverified":
                e.state = "dead"
                e.note = f"复核仍失败（{e.note}）"
        if (i // size) % 5 == 0 or i + size >= len(cand):
            print(f"  进度 {min(i + size, len(cand))}/{len(cand)}", flush=True)
        if pause and i + size < len(cand):
            time.sleep(pause)
    back = sum(1 for e in cand if e.state == "verified")
    print(f"  补核通过 {back} 条，用时 {time.perf_counter() - t0:.0f}s", flush=True)


def run_probes(entries: list[Entry], cfg: dict) -> None:
    preflight_dns(entries, cfg)

    todo = [e for e in entries if e.state == "pending"]
    t0 = time.perf_counter()

    def work(e: Entry) -> Entry:
        return probe(e, cfg)

    def run_batch(items: list[Entry], label: str, workers: int | None = None) -> None:
        """连续打几千条会把出口 IP 打成 403，之后所有源都看起来是死的。
        小批量 + 批间冷却是唯一能拿到真实结果的办法。"""
        if not items:
            return
        n = len(items)
        size = batch or n
        done = 0
        for i in range(0, n, size):
            with ThreadPoolExecutor(max_workers=workers or cfg["concurrency"]) as pool:
                list(pool.map(work, items[i:i + size]))
            done += len(items[i:i + size])
            print(f"  {label} {done}/{n}", flush=True)
            if pause and i + size < n:
                time.sleep(pause)

    batch = max(0, int(cfg.get("batch_size", 0) or 0))
    pause = max(0.0, float(cfg.get("batch_pause", 0) or 0))
    if batch:
        print(f"  限速：每批 {batch} 条，批间冷却 {pause:.0f}s，并发 {cfg['concurrency']}")
    run_batch(todo, "进度")

    # 第二轮：只重试第一轮因为网络抖动失败的，降低偶发超时造成的误杀
    retries = int(cfg.get("retries", 0))
    for r in range(retries):
        dead = [e for e in entries if e.state == "dead" and e.note != "域名解析失败"]
        if not dead:
            break
        print(f"  重试第 {r + 1} 轮，{len(dead)} 条")
        run_batch(dead, "重试")

    # 首轮结束后才复核。之前试过冷却 6 秒后用 8 并发立刻重打，一条都救不回来：
    # 恢复窗口是分钟级，而且并发一高又把自己打成 403。
    recheck_soft(entries, cfg)

    verify_liveness(entries, cfg)

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


def write_report(path: Path, entries: list[Entry], cfg: dict,
                 kept: list[Entry] | None = None) -> None:
    verified = [e for e in entries if e.state == "verified"]
    unverified = [e for e in entries if e.state == "unverified"]
    dead = [e for e in entries if e.state == "dead"]

    basis = kept if kept is not None else [e for e in entries if e.ok]
    names = {e.name for e in basis}
    drop = bool(cfg.get("drop_unverified", False)) and (
        not IS_CI or bool(cfg.get("drop_unverified_in_ci", False))
    )
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M (UTC+8)")

    out = [
        "# 直播源清洗报告",
        "",
        f"生成时间：{now}",
        "",
        "| 指标 | 数值 |",
        "| --- | --- |",
        f"| 原始条目 | {len(entries)} |",
        f"| 实测通过 | {len(verified)} |",
        f"| 未通过校验（{'已移出订阅' if drop else '保留待核'}） | {len(unverified)} |",
        f"| 本机判定不可达 | {len(dead)} |",
        f"| 写入订阅 | {len(basis)} |",
        f"| 有效频道数 | {len(names)} |",
    ]
    if verified:
        avg = sum(e.ms for e in verified) / len(verified)
        out.append(f"| 平均响应 | {avg:.0f} ms |")

    if unverified:
        heading = "未通过校验（已移出订阅）" if drop else "保留但未校验"
        out += ["", f"## {heading}", "", "| 频道 | 原因 |", "| --- | --- |"]
        for e in unverified[:30]:
            out.append(f"| {e.name} | {e.note} |")

    if dead:
        out += ["", "## 本机判定不可达（节选）", "", "| 频道 | 状态 | 地址 |", "| --- | --- | --- |"]
        for e in dead[:60]:
            out.append(f"| {e.name} | {e.note} | `{e.url[:70]}` |")
        if len(dead) > 60:
            out.append(f"| … | 另有 {len(dead) - 60} 条 | |")

    kept_urls = {e.url for e in basis}
    removed = [e for e in entries if e.url not in kept_urls]
    if removed:
        tally: dict[str, int] = {}
        for e in removed:
            key = e.note or ("每频道线路上限" if e.state == "verified" else "未通过校验")
            key = key.replace("|", "／")
            tally[key] = tally.get(key, 0) + 1
        out += ["", "## 移出订阅的原因", "", "| 原因 | 条数 |", "| --- | --- |"]
        for k, v in sorted(tally.items(), key=lambda x: -x[1])[:15]:
            out.append(f"| {k} | {v} |")
        out += ["", f"完整逐条清单见 `removed.tsv`（{len(removed)} 条）。",
                "未通过校验但未判死的源另存于 `pending.m3u`，需要时可自行加回。"]

    out += [
        "",
        "## 判定边界",
        "",
        "报告只反映**跑清洗那台机器的网络**能连到什么，不是源站的最终状态。",
        "403/429 里常混着出口 IP 限流或网络策略拦截——典型特征是 1ms 返回、空响应体、",
        "没有 Server 头，TCP 甚至从未真正建连。这类不算源站判死，换个网络或播放器可能照样能播。",
        "移出的条目都在 `removed.tsv` 留了完整地址和原始属性，确认某条其实能播时可直接加回。",
    ]

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
    ap.add_argument("--recheck", action="store_true",
                    help="读上一轮 detail.tsv，网络恢复后低速补核失败队列，不重跑主探测")
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

    out_dir = root / cfg["output_dir"]
    if args.recheck:
        print("\n[2/4] 网络恢复后低速补核（不重跑主探测）")
        state = load_state(out_dir / "detail.tsv")
        hit = 0
        for e in entries:
            if e.url in state:
                e.state, e.note = state[e.url]
                if e.state == "pending":
                    e.state = "unverified"
                hit += 1
        print(f"  从 detail.tsv 恢复 {hit}/{len(entries)} 条判定")
        recheck_slow(entries, cfg)
        verify_liveness(entries, cfg)
    else:
        print("\n[2/4] 探测可用性")
        run_probes(entries, cfg)

    print("\n[3/4] 整理输出")
    drop = bool(cfg.get("drop_unverified", False)) and (
        not IS_CI or bool(cfg.get("drop_unverified_in_ci", False))
    )
    good = sorted(
        [e for e in entries if (e.state == "verified" if drop else e.ok)],
        key=lambda e: e.sort_key,
    )
    good = apply_limit_per_channel(good, int(cfg.get("max_per_channel", 0)))
    print(f"  策略：{'只留实测通过，失败即剔除' if drop else '保守模式，保留未校验'}")
    if IS_CI and cfg.get("drop_unverified") and not cfg.get("drop_unverified_in_ci"):
        print("  Actions 是境外 IP，自动切保守模式，避免把只允许大陆访问的源整批误删")

    write_m3u(out_dir / "all.m3u", good, cfg)
    write_m3u(out_dir / "all_status.m3u", good, cfg, with_status=True)

    if drop:
        held = [e for e in entries if e.state == "unverified"]
        if held:
            write_m3u(out_dir / "pending.m3u", held, cfg, with_status=True)
        kept_urls = {g.url for g in good}
        removed = [e for e in entries if e.url not in kept_urls]
        if removed:
            write_detail(out_dir / "removed.tsv", removed)
        print(f"  移出订阅 {len(removed)} 条 → removed.tsv；"
              f"其中未判死的 {len(held)} 条另存 → pending.m3u")

    # 主订阅：只含 source/ 里手工挑选的源，保持原文件名不变，订阅地址不受影响
    local = [e for e in good if e.origin == "local"]
    if cfg.get("primary_output") and local:
        # CI 上跑的是保守模式，结果里混着大量「境外连不上、境内能播」的源。
        # 用它覆盖本地确认过的订阅，等于把好源又塞回去，所以直接跳过。
        if IS_CI and cfg.get("drop_unverified") and not cfg.get("drop_unverified_in_ci"):
            print(f"  Actions 保守模式：跳过主订阅 {cfg['primary_output']}，"
                  "避免用境外 IP 的结果覆盖本地确认版")
        else:
            write_m3u(root / cfg["primary_output"], local, cfg)
            print(f"  主订阅 {cfg['primary_output']}：{len(local)} 条")

    groups = sorted({e.group for e in good if e.group})
    if cfg.get("group_files", True):
        for g in groups:
            sub = [e for e in good if e.group == g]
            safe = re.sub(r'[\\/:*?"<>|\s]+', "_", g)[:40]
            write_m3u(out_dir / "groups" / f"{safe}.m3u", sub, cfg)

    # 分类以「分组」为单位整体判定。之前按频道名做子串匹配，
    # 会把同一个分组拆散：比如「浙江频道」里的「浙江教科影视」命中"影视"
    # 跑进 difang.m3u，「浙江新闻」却留在 other.m3u。
    group_owner: dict[str, str] = {}
    for cat in cfg.get("categories", []):
        keys = [k.lower() for k in cat.get("match", [])]
        for g in groups:
            if g in group_owner or not g:
                continue
            if any(k in g.lower() for k in keys):
                group_owner[g] = cat["file"]

    matched: set[str] = set()
    for cat in cfg.get("categories", []):
        keys = [k.lower() for k in cat.get("match", [])]
        sub = [
            e for e in good
            if group_owner.get(e.group) == cat["file"]
            or (e.group not in group_owner and any(k in e.name.lower() for k in keys))
        ]
        if sub:
            write_m3u(out_dir / cat["file"], sub, cfg)
            matched.update(e.url for e in sub)
    rest = [e for e in good if e.url not in matched]
    if rest:
        write_m3u(out_dir / "other.m3u", rest, cfg)

    write_report(out_dir / "report.md", entries, cfg, good)
    write_detail(out_dir / "detail.tsv", entries)

    print("\n[4/4] 完成")
    v = sum(1 for e in entries if e.state == "verified")
    u = sum(1 for e in entries if e.state == "unverified")
    d = sum(1 for e in entries if e.state == "dead")
    print(f"  实测通过 {v}　未通过校验 {u}　本机不可达 {d}　写入订阅 {len(good)} 条")
    print(f"  → {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
