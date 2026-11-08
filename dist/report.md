# 直播源清洗报告

生成时间：2026-11-09 07:23 (UTC+8)

| 指标 | 数值 |
| --- | --- |
| 原始条目 | 1422 |
| 实测通过 | 482 |
| 未通过校验（保留待核） | 75 |
| 本机判定不可达 | 865 |
| 写入订阅 | 557 |
| 有效频道数 | 496 |
| 平均响应 | 1185 ms |

## 保留但未校验

| 频道 | 原因 |
| --- | --- |
| 西峰综合 | 播放列表停滞（循环回放） |
| 凤凰香港 | 播放列表停滞（循环回放） |
| 凤凰香港 | 播放列表停滞（循环回放） |
| 华丽翡翠台 | 点播列表（非直播） |
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

## 本机判定不可达（节选）

| 频道 | 状态 | 地址 |
| --- | --- | --- |
| CCTV-2 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://101.35.240.114:88/live.php?id=CCTV2` |
| CCTV-16 | 返回非流内容 | `http://74.91.26.218:82/live/cctv16hd.m3u8` |
| 黑龙江卫视 | URLError | `https://idclive.hljtv.com:4430/live/hljws_own.m3u8` |
| 黑龙江文体 | URLError | `https://idclive.hljtv.com:4430/live/hljwy_hd.m3u8` |
| 黑龙江都市 | URLError | `https://idclive.hljtv.com:4430/live/dushi_hd.m3u8` |
| 绍兴电视台公共 | 连接超时 | `http://live.shaoxing.com.cn/video/s10001-sxtv2/index.m3u8?%E5%85%B3%E6` |
| 新野综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/11329-1.m3u8` |
| 永城综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/11481-1.m3u8` |
| 荥阳综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/10182-1.m3u8` |
| 剑阁综合 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel105549/pla` |
| 广元公共 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel101257/pla` |
| 宁夏公共 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://hls.ningxiahuangheyun.com/live/nxgg1M.m3u8` |
| 宁夏文旅 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://hls.ningxiahuangheyun.com/live/nxwl1M.m3u8` |
| 美亚电影 | 连接超时 | `http://iptv.4666888.xyz/iptv2A.php?id=30` |
| 凤凰资讯 [FLV] | 返回非流内容 | `http://43.152.224.209/qctv.fengshows.cn/live/0701pin72.flv` |
| Jade | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-1/master.m3u8` |
| Asian Drama | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-11/master.m3u8` |
| Mei Ah Movie Channel | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-2/master.m3u8` |
| Arena Sport Premium M3 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://telekomsrbije.com:2095/play/lhpjmkfVyhON1JAiZCx7vgvje3t-Jiqa5d9` |
| TVS Boxing (360p) | 域名解析失败 | `https://rpn.bozztv.com/gusa/gusa-tvsboxing/index.m3u8` |
| 北京卫视4K | HTTP 404 | `http://139.ye23.vip/dl/btv2502.php?id=bjws4` |
| 广东卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=广东卫视4K` |
| 深圳卫视4K | 返回非流内容 | `http://nn.7x9d.cn/深圳最新.php?id=szws4k` |
| 山东卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=山东卫视4K` |
| 四川卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=四川卫视4K` |
| CCTV4K真4K | 连接被拒 | `http://vip1.xinketongxun.fun:8082/tsfile/live/1026_1.m3u8` |
| CCTV1 | URLError | `http://101.35.240.114:88/live.php?id=CCTV1` |
| CCTV2 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV2` |
| CCTV3 | URLError | `http://101.35.240.114:88/live.php?id=CCTV3` |
| CCTV4 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV4` |
| CCTV5 | URLError | `http://101.35.240.114:88/live.php?id=CCTV5` |
| CCTV5+ | 连接超时 | `http://148.135.93.213/live.php?id=CCTV5p` |
| CCTV6 | URLError | `http://101.35.240.114:88/live.php?id=CCTV6` |
| CCTV7 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV7` |
| CCTV8 | URLError | `http://101.35.240.114:88/live.php?id=CCTV8` |
| CCTV9 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV9` |
| CCTV10 | URLError | `http://101.35.240.114:88/live.php?id=CCTV10` |
| CCTV11 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV11` |
| CCTV12 | URLError | `http://101.35.240.114:88/live.php?id=CCTV12` |
| CCTV13 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV13` |
| CCTV14 | URLError | `http://101.35.240.114:88/live.php?id=CCTV14` |
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
| … | 另有 805 条 | |

## 移出订阅的原因

| 原因 | 条数 |
| --- | --- |
| 连接超时 | 196 |
| HTTP 404 | 144 |
| 连接被拒 | 144 |
| TLS 握手失败 | 71 |
| URLError | 68 |
| 复核仍失败（HTTP 403（限流/地区限制）） | 63 |
| 域名解析失败 | 52 |
| HTTP 500 | 42 |
| HTTP 302 | 35 |
| 返回非流内容 | 27 |
| HTTP 418 | 8 |
| HTTP 523 | 5 |
| HTTP 400 | 3 |
| HTTP 502 | 2 |
| 播放列表为空 | 2 |

完整逐条清单见 `removed.tsv`（865 条）。
未通过校验但未判死的源另存于 `pending.m3u`，需要时可自行加回。

## 判定边界

报告只反映**跑清洗那台机器的网络**能连到什么，不是源站的最终状态。
403/429 里常混着出口 IP 限流或网络策略拦截——典型特征是 1ms 返回、空响应体、
没有 Server 头，TCP 甚至从未真正建连。这类不算源站判死，换个网络或播放器可能照样能播。
移出的条目都在 `removed.tsv` 留了完整地址和原始属性，确认某条其实能播时可直接加回。
