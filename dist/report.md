# 直播源清洗报告

生成时间：2026-11-08 07:11 (UTC+8)

| 指标 | 数值 |
| --- | --- |
| 原始条目 | 1317 |
| 实测通过 | 406 |
| 未通过校验（保留待核） | 72 |
| 本机判定不可达 | 839 |
| 写入订阅 | 478 |
| 有效频道数 | 425 |
| 平均响应 | 1250 ms |

## 保留但未校验

| 频道 | 原因 |
| --- | --- |
| 广东体育 | 播放列表停滞（循环回放） |
| 民视 | 非 http(s) 协议（rtmp） |
| 台视 | 非 http(s) 协议（rtmp） |
| 中视 | 非 http(s) 协议（rtmp） |
| 华视 | 非 http(s) 协议（rtmp） |
| 三立戏剧 | 播放列表停滞（循环回放） |
| 非凡新闻 | 非 http(s) 协议（rtmp） |
| 东森超视 | 非 http(s) 协议（rtmp） |
| MOMO TV | 非 http(s) 协议（rtmp） |
| 纬来日本 | 非 http(s) 协议（rtmp） |
| 纬来体育 | 非 http(s) 协议（rtmp） |
| 纬来育乐 | 非 http(s) 协议（rtmp） |
| 纬来精采 | 播放列表停滞（循环回放） |
| TVBS新闻台 | 播放列表停滞（循环回放） |
| 八大戏剧台 | 点播列表（非直播） |
| ASTRO AOD | 播放列表停滞（循环回放） |
| DAZN体育1 | 非 http(s) 协议（rtmp） |
| DAZN体育2 | 非 http(s) 协议（rtmp） |
| NewTV 超级综艺 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 金牌综艺 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 魅力潇湘 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 古装剧场 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 怡伴健康 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 潮妈辣婆 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 军旅剧场 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 军事评论 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 中国功夫 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 农业致富 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 家庭剧场 | IPv6 源，Actions 无 IPv6 无法校验 |
| NewTV 惊悚悬疑 | IPv6 源，Actions 无 IPv6 无法校验 |

## 本机判定不可达（节选）

| 频道 | 状态 | 地址 |
| --- | --- | --- |
| Jade | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-1/master.m3u8` |
| CCTV2 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://101.35.240.114:88/live.php?id=CCTV2` |
| Asian Drama | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-11/master.m3u8` |
| Mei Ah Movie Channel | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-2/master.m3u8` |
| CCTV-16 HD (1080p) | 返回非流内容 | `http://74.91.26.218:82/live/cctv16hd.m3u8` |
| Arena Sport Premium M3 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://telekomsrbije.com:2095/play/lhpjmkfVyhON1JAiZCx7vgvje3t-Jiqa5d9` |
| 北京卫视4K | HTTP 404 | `http://139.ye23.vip/dl/btv2502.php?id=bjws4` |
| 广东卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=广东卫视4K` |
| 深圳卫视4K | 返回非流内容 | `http://nn.7x9d.cn/深圳最新.php?id=szws4k` |
| 山东卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=山东卫视4K` |
| 四川卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=四川卫视4K` |
| CCTV4K真4K | 连接超时 | `http://vip1.xinketongxun.fun:8082/tsfile/live/1026_1.m3u8` |
| CCTV1 | HTTP 660 | `http://101.35.240.114:88/live.php?id=CCTV1` |
| CCTV2 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV2` |
| CCTV4 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV4` |
| CCTV5+ | 连接超时 | `http://148.135.93.213/live.php?id=CCTV5p` |
| CCTV7 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV7` |
| CCTV9 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV9` |
| CCTV11 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV11` |
| CCTV13 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV13` |
| CCTV15 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV15` |
| CCTV16 | 连接超时 | `http://101.35.240.114:88/live.php?id=CCTV16` |
| CCTV17 | 连接超时 | `http://74.48.192.96:82/live.php?id=CCTV17` |
| CCTV-兵器科技 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.98:5140` |
| CCTV-世界地理 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.93:5140` |
| CCTV-风云足球 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.96:5140` |
| CCTV-风云音乐 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.87:5140` |
| CCTV-风云剧场 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.89:5140` |
| CCTV-第一剧场 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.86:5140` |
| CCTV-怀旧剧场 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.90:5140` |
| CCTV-文化精品 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.81:5140` |
| CCTV-女性时尚 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.94:5140` |
| CCTV-卫生健康 | URLError | `http://nas.hssvm.com:8888/udp/225.1.1.210:5002` |
| CCTV-央视台球 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.80:5140` |
| CCTV-央视高网 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.95:5140` |
| CCTV-电视指南 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.97:5140` |
| 中国天气 | 连接超时 | `http://hls.weathertv.cn/tslslive/qCFIfHB/hls/live_sd.m3u8` |
| 中国交通 | 连接被拒 | `http://drive.mxmy.net:8888/udp/239.3.1.188:8001` |
| 直播中国 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://gcalic.v.myalicdn.com/gc/wgw05_1/index.m3u8?contentid=28201805` |
| CETV-1 综合教育 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.220.198:5140` |
| CETV-2 空中课堂 | 域名解析失败 | `http://www.lizhinas.top:1009/rtp/239.252.219.73:5140` |
| CETV-3 教育服务 | URLError | `http://rrs01.hw.gmcc.net:8088/PLTV/81/224/3221226722/1.m3u8` |
| CETV-4 职业教育 | URLError | `http://rrs01.hw.gmcc.net:8088/PLTV/81/224/3221226724/1.m3u8` |
| CGTN俄语 | 连接超时 | `http://russian-livews.cgtn.com/hls/LSvexABhNipibK5KRuUkvHZ7220802LSTez` |
| CCTV1 | URLError | `http://iptv.huuc.edu.cn/hls/cctv1hd.m3u8` |
| CCTV2 | URLError | `http://iptv.huuc.edu.cn/hls/cctv2hd.m3u8` |
| CCTV3 | URLError | `http://iptv.huuc.edu.cn/hls/cctv3hd.m3u8` |
| CCTV4 | URLError | `http://iptv.huuc.edu.cn/hls/cctv4hd.m3u8` |
| CCTV5 | URLError | `http://iptv.huuc.edu.cn/hls/cctv5hd.m3u8` |
| CCTV6 | URLError | `http://iptv.huuc.edu.cn/hls/cctv6hd.m3u8` |
| CCTV7 | URLError | `http://iptv.huuc.edu.cn/hls/cctv7hd.m3u8` |
| CCTV8 | URLError | `http://iptv.huuc.edu.cn/hls/cctv8hd.m3u8` |
| CCTV9 | URLError | `http://iptv.huuc.edu.cn/hls/cctv9hd.m3u8` |
| CCTV10 | URLError | `http://iptv.huuc.edu.cn/hls/cctv10hd.m3u8` |
| CCTV11 | URLError | `http://iptv.huuc.edu.cn/hls/cctv11hd.m3u8` |
| CCTV12 | URLError | `http://iptv.huuc.edu.cn/hls/cctv12hd.m3u8` |
| CCTV13 | URLError | `http://iptv.huuc.edu.cn/hls/cctv13hd.m3u8` |
| CCTV14 | URLError | `http://iptv.huuc.edu.cn/hls/cctv14hd.m3u8` |
| CCTV15 | HTTP 404 | `http://p.ytelc.com/169l/0/cctv.php?id=cctv15` |
| CCTV16 | HTTP 404 | `http://p.ytelc.com/169l/0/cctv.php?id=cctv16` |
| … | 另有 779 条 | |

## 移出订阅的原因

| 原因 | 条数 |
| --- | --- |
| 连接超时 | 203 |
| HTTP 404 | 142 |
| 连接被拒 | 129 |
| TLS 握手失败 | 71 |
| 复核仍失败（HTTP 403（限流/地区限制）） | 57 |
| URLError | 52 |
| 域名解析失败 | 51 |
| HTTP 500 | 42 |
| HTTP 302 | 36 |
| 返回非流内容 | 27 |
| HTTP 418 | 8 |
| RemoteDisconnected | 7 |
| HTTP 523 | 5 |
| HTTP 400 | 3 |
| HTTP 502 | 2 |

完整逐条清单见 `removed.tsv`（839 条）。
未通过校验但未判死的源另存于 `pending.m3u`，需要时可自行加回。

## 判定边界

报告只反映**跑清洗那台机器的网络**能连到什么，不是源站的最终状态。
403/429 里常混着出口 IP 限流或网络策略拦截——典型特征是 1ms 返回、空响应体、
没有 Server 头，TCP 甚至从未真正建连。这类不算源站判死，换个网络或播放器可能照样能播。
移出的条目都在 `removed.tsv` 留了完整地址和原始属性，确认某条其实能播时可直接加回。
