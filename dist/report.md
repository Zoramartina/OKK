# 直播源清洗报告

生成时间：2026-11-12 10:04 (UTC+8)

| 指标 | 数值 |
| --- | --- |
| 原始条目 | 1532 |
| 实测通过 | 565 |
| 未通过校验（保留待核） | 76 |
| 本机判定不可达 | 891 |
| 写入订阅 | 641 |
| 有效频道数 | 572 |
| 平均响应 | 1117 ms |

## 保留但未校验

| 频道 | 原因 |
| --- | --- |
| 天祝综合 | 播放列表停滞（循环回放） |
| 永昌综合 | 播放列表停滞（循环回放） |
| NOW新闻台 | 播放列表停滞（循环回放） |
| 长江大桥 | 点播列表（非直播） |
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
| CCTV-16 | 返回非流内容 | `http://74.91.26.218:82/live/cctv16hd.m3u8` |
| 海南卫视 | 返回非流内容 | `http://nn.7x9d.cn/地方台8563/海南.php?id=hnws` |
| 黑龙江卫视 | URLError | `https://idclive.hljtv.com:4430/live/hljws_own.m3u8` |
| 黑龙江农业科教频道 | URLError | `https://idclive.hljtv.com:4430/live/hljgg_hd.m3u8` |
| 黑龙江文体 | URLError | `https://idclive.hljtv.com:4430/live/hljwy_hd.m3u8` |
| 黑龙江都市 | URLError | `https://idclive.hljtv.com:4430/live/dushi_hd.m3u8` |
| 绍兴电视台公共 | 连接超时 | `http://live.shaoxing.com.cn/video/s10001-sxtv2/index.m3u8?%E5%85%B3%E6` |
| 新野综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/11329-1.m3u8` |
| 永城综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/11481-1.m3u8` |
| 荥阳综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/10182-1.m3u8` |
| 海南公共 | 返回非流内容 | `http://nn.7x9d.cn/地方台8563/海南.php?id=ggpd` |
| 海南少儿 | 返回非流内容 | `http://nn.7x9d.cn/地方台8563/海南.php?id=sepd` |
| 海南文旅 | 返回非流内容 | `http://nn.7x9d.cn/地方台8563/海南.php?id=wlpd` |
| 海南新闻 | 返回非流内容 | `http://nn.7x9d.cn/地方台8563/海南.php?id=xwpd` |
| 海南自贸 | 返回非流内容 | `http://nn.7x9d.cn/地方台8563/海南.php?id=jjpd` |
| 剑阁综合 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel105549/pla` |
| 广元公共 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel101257/pla` |
| 广元综合 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel100999/pla` |
| 旺苍新闻综合 | URLError | `http://channel.wcrmt.cn:80/nmip-media/channellive/channel105268/playli` |
| 朝天综合 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel104601/pla` |
| 松潘新闻综合 | URLError | `http://live.spccmc.com:90/live/spxwzh.m3u8` |
| 宁夏公共 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://hls.ningxiahuangheyun.com/live/nxgg1M.m3u8` |
| 宁夏文旅 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://hls.ningxiahuangheyun.com/live/nxwl1M.m3u8` |
| LIVE三立 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/setnewsrtmp/playlist.m3u8` |
| TVBS新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/tvbsnewsqt/playlist.m3u8` |
| 三立新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/iNEWS/playlist.m3u8` |
| 东森新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/EBCNews/playlist.m3u8` |
| 中天新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/CtiNEWS1/playlist.m3u8` |
| 中视新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/ctvnewsqt/playlist.m3u8` |
| 华视新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/ctsnewsqt/playlist.m3u8` |
| 民视新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/ftvnewsqt/playlist.m3u8` |
| 纬来体育 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://hlsz.yjjcfw.com/live/vl.m3u8?expire=1786948372&sign=2e4a56b89f` |
| 香港卫视 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://webcast.hkstv.tv/livestream/mutfysrq/playlist.m3u8` |
| NewTV古装剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c58_fast_947_1080P_t10/c` |
| NewTV大家剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c58_fast_975_1080P_t10/c` |
| NewTV家庭剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c59_fast_999_1080P_t10/c` |
| NewTV泰语剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c58_fast_949_1080P_t10/c` |
| NewTV爱情剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c59_fast_967_1080P_t10/c` |
| 美亚电影 | RemoteDisconnected | `http://iptv.4666888.xyz/iptv2A.php?id=30` |
| Jade | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-1/master.m3u8` |
| CCTV2 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://101.35.240.114:88/live.php?id=CCTV2` |
| Asian Drama | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-11/master.m3u8` |
| Mei Ah Movie Channel | HTTP 404 | `http://103.172.187.30:12000/stream/mytv/null-2/master.m3u8` |
| 五星体育 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://101.35.240.114:88/live.php?id=五星体育` |
| CCTV-5 | 连接超时 | `http://207.56.13.146:81/cdnlive/cctv5.m3u8` |
| CCTV-16 | 连接超时 | `http://207.56.13.146:81/cdnlive/cctv16.m3u8` |
| Arena Sport Premium M3 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://telekomsrbije.com:2095/play/lhpjmkfVyhON1JAiZCx7vgvje3t-Jiqa5d9` |
| Eurosport (720p) | HTTP 404 | `https://drk6xq0vhn.gpcdn.net/live/euro_sports_hd_abr/index.m3u8` |
| 北京卫视4K | HTTP 404 | `http://139.ye23.vip/dl/btv2502.php?id=bjws4` |
| 广东卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=广东卫视4K` |
| 深圳卫视4K | 返回非流内容 | `http://nn.7x9d.cn/深圳最新.php?id=szws4k` |
| 山东卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=山东卫视4K` |
| 四川卫视4K | HTTP 404 | `http://101.35.240.114:88/live.php?id=四川卫视4K` |
| CCTV1 | HTTP 660 | `http://101.35.240.114:88/live.php?id=CCTV1` |
| CCTV2 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV2` |
| CCTV3 | HTTP 660 | `http://101.35.240.114:88/live.php?id=CCTV3` |
| CCTV4 | 连接超时 | `http://148.135.93.213/live.php?id=CCTV4` |
| CCTV5 | HTTP 660 | `http://101.35.240.114:88/live.php?id=CCTV5` |
| CCTV5+ | 连接超时 | `http://148.135.93.213/live.php?id=CCTV5p` |
| CCTV6 | HTTP 660 | `http://101.35.240.114:88/live.php?id=CCTV6` |
| … | 另有 831 条 | |

## 移出订阅的原因

| 原因 | 条数 |
| --- | --- |
| 连接超时 | 199 |
| 连接被拒 | 140 |
| HTTP 404 | 138 |
| 复核仍失败（HTTP 403（限流/地区限制）） | 83 |
| TLS 握手失败 | 71 |
| URLError | 57 |
| 域名解析失败 | 51 |
| HTTP 500 | 42 |
| 返回非流内容 | 38 |
| HTTP 302 | 35 |
| HTTP 660 | 13 |
| HTTP 418 | 8 |
| HTTP 523 | 5 |
| HTTP 400 | 3 |
| RemoteDisconnected | 2 |

完整逐条清单见 `removed.tsv`（891 条）。
未通过校验但未判死的源另存于 `pending.m3u`，需要时可自行加回。

## 判定边界

报告只反映**跑清洗那台机器的网络**能连到什么，不是源站的最终状态。
403/429 里常混着出口 IP 限流或网络策略拦截——典型特征是 1ms 返回、空响应体、
没有 Server 头，TCP 甚至从未真正建连。这类不算源站判死，换个网络或播放器可能照样能播。
移出的条目都在 `removed.tsv` 留了完整地址和原始属性，确认某条其实能播时可直接加回。
