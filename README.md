# OKK 直播源

一个只用 Python 标准库的直播源清洗仓库：`source/` 里放手工维护的源，脚本逐条实测，根目录 `tv.m3u` 是生成的订阅文件，播放器只填这一个地址。

```
https://raw.githubusercontent.com/Zoramartina/OKK/main/tv.m3u
```

## 当前构成

共 **160 条**，按分组：

| 分组 | 条数 | 内容 |
| --- | --- | --- |
| 央视频道 | 18 | CCTV-1~17，含 CCTV-5+，一套一个源 |
| 卫视频道 | 35 | 30 个省级卫视 + 东方/江苏/浙江/深圳/湖南 5 个 4K 版 |
| 地方·各省 | 83 | 省内地市、县级台，按省分组 |
| 体育·赛事台 | 9 | 英文解说：Cricket Gold、Eurosport 1、Fox Sports、NBC Sports、NHL、Willow、beIN XTRA 等 |
| 电影频道 | 14 | CHC 动作/家庭/电影、美亚电影、Cinemax、Paramount、Showtime、Universal、AXN、FILMBOX+ |
| 凤凰卫视 | 1 | 凤凰资讯（FLV 720p） |

中国台湾、中国香港频道已全部移除。凤凰中文、凤凰香港暂时没有可用源，原因见下文。

分类文件在 `dist/`，主订阅 `tv.m3u` 是完整版：

```
dist/cctv.m3u     央视频道 18
dist/weishi.m3u   卫视频道 35
dist/difang.m3u   地方台 83
dist/sports.m3u   英文体育 9
dist/movie.m3u    电影频道 14
dist/gangao.m3u   凤凰资讯 1
```

## 本次调整说明

**地方台扩到 118 个。** 从 27 份仍在更新的公开列表里提取候选，按频道名去重后逐条实测；省级卫视另按已知可用的 IPTV 源地址规律补测了一批线路。当前覆盖 30 个省级卫视、26 个省的省市县级台。内蒙古、宁夏、新疆、西藏、海南、福建 6 个省级卫视的候选线路全部不可达，没有硬凑。

**央视只留主频道。** CGTN 多语种、央视付费频道（兵器科技、台球、风云剧场等）、CNR 广播、CCTV+、CCTV-8K 全部移出。原列表里的 CCTV-8 实际指向 `cctv8k.m3u8`（8K 超高清），不是电视剧频道，已换成真正的 CCTV-8。

**港台删除，凤凰保留一条。** 台湾 17 条、香港 3 条、港澳台混合 3 条全部移除。凤凰卫视的公网 HLS 已经大面积失效：ifeng 官方 master 能返回 720p 两档码率，但子列表 `_tv1.m3u8` 全部 404；`hls-gateway.vpstv.net` 返回 403；`cdn6.163189.xyz` 返回的是网页；`r.jdshipin.com` 短链超时。最后只有一条实测可用：

```
凤凰资讯  http://43.152.224.209/qctv.fengshows.cn/live/0701pin72.flv
```

这是 FLV 流（H264 / 1280x720），VLC、PotPlayer 能播；TiviMate 和部分电视盒子只认 HLS，可能播不了，频道名标了 `[FLV]`。

**体育只留英文。** ESPN 拉美系列（西语）、DAZN 葡萄牙、Eurosport 波兰/捷克/匈牙利/俄罗斯/德国/葡萄牙版、FightBox Poland、Persiana Fight、TVS Boxing、Arena Sport 塞尔维亚等全部移出。TNT Sports 1~4 的公开源整组 404，ESPN 美国 HD 线路 TCP 不通，能通的只有拉美西语版，按“只留英文”的要求没有放进来。

**电影新增 7 个。** 保留中文的 CHC 系列、美亚电影，新增 Cinemax、Paramount、Showtime、Universal、AXN、FILMBOX+ 等英文频道。阿拉伯语 Rotana、拉美西语 TCM/AMC/AXN、东欧小语种和 240p/480p 低清源已剔除。

逐条移除记录在 `dist/removed.tsv`，完整说明在 `dist/report.md`。

## 文件结构

| 路径 | 说明 |
| --- | --- |
| `source/curated.m3u` | **手工维护区**，本次精选的 160 条源，改这里才算数 |
| `archive/` | 上一版 1300 条归档，只作追溯，不参与清洗 |
| `tv.m3u` | 生成物，播放器订阅地址，别手改 |
| `dist/` | 分类文件、调整报告、移除清单 |
| `scripts/clean.py` | 清洗脚本，纯标准库 |
| `config.json` | 清洗配置：输入 `source/`，输出 `dist/`，主输出 `tv.m3u` |
| `.github/workflows/clean.yml` | 每天北京时间 03:00 自动跑一遍 |

## 怎么维护

加频道：往 `source/curated.m3u` 里按 M3U 格式追加，`#EXTINF` 后跟地址，需要 UA 或 Referer 就写 `http-user-agent`、`http-referer` 属性。改完提交，Actions 会重跑清洗；也可以本地跑：

```bash
python scripts/clean.py
```

删频道：直接从 `source/curated.m3u` 删掉对应条目，再跑一次清洗。

不要在 `tv.m3u` 上改，它是生成物，下次清洗会被覆盖。

## 自动清洗

`.github/workflows/clean.yml` 每天 UTC 19:00（北京时间 03:00）跑一次，也支持手动触发。脚本会重新探测 `source/` 里的每一条源，通过的写进 `tv.m3u` 和 `dist/`，失败的剔除，结果提交回仓库。

CI 用的是境外 runner，跑的是保守模式（`drop_unverified_in_ci: false`）：探不到的源不会直接删，只更新报告。真正严格的剔除在本机跑 `python scripts/clean.py` 才生效。

仓库 Settings → Actions → General 里要把 Workflow permissions 设成 **Read and write**，否则定时任务提交会 403。

## 判定标准

一条源要同时过四关才算可用：

1. TCP 能建连（排除域名解析失败、端口不通）
2. 返回的是播放列表或 TS 流，不是网页、404、403
3. 列表里能追到分片
4. 间隔 12 秒再抓一次，媒体序列号或末尾分片名在前进（排除循环回放的僵尸列表）

“可用”只代表跑清洗这台机器能拉到流。换网络、换播放器，结论可能不同；地方县级台多为地方广电 CDN，跨省访问可能变慢。凤凰资讯那条是 FLV，对播放器有要求。

## 已知限制

- 凤凰中文、凤凰香港：公网 HLS 源全部失效，只有凤凰资讯的 FLV 可用
- TNT Sports、ESPN 英文版：现有公开源 404 或地区限制，没有可用线路
- 内蒙古、宁夏、新疆、西藏、海南、福建卫视：候选源全部不可达
- 央视多数源只返回 media playlist，读不出 `RESOLUTION`，画质按源命名和实测码率判断
