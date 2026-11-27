# 直播源清洗报告

生成时间：2026-11-27 10:49 (UTC+8)

| 指标 | 数值 |
| --- | --- |
| 原始条目 | 1532 |
| 实测通过 | 556 |
| 未通过校验（保留待核） | 82 |
| 本机判定不可达 | 894 |
| 写入订阅 | 638 |
| 有效频道数 | 569 |
| 平均响应 | 1154 ms |

## 保留但未校验

| 频道 | 原因 |
| --- | --- |
| 南宁影视娱乐 | 播放列表停滞（循环回放） |
| 天祝综合 | 播放列表停滞（循环回放） |
| 永昌综合 | 播放列表停滞（循环回放） |
| 西峰综合 | 播放列表停滞（循环回放） |
| NOW新闻台 | 播放列表停滞（循环回放） |
| RTHK31 | 点播列表（非直播） |
| RTHK32 | 点播列表（非直播） |
| TVB星河3 | 播放列表停滞（循环回放） |
| 无线新闻台 | 点播列表（非直播） |
| 天映新加坡 | 播放列表停滞（循环回放） |
| 天映经典台2 | 播放列表停滞（循环回放） |
| 凤凰香港 | 播放列表停滞（循环回放） |
| 凤凰香港 | 播放列表停滞（循环回放） |
| 无线新闻 | 点播列表（非直播） |
| TVB星河 | 播放列表停滞（循环回放） |
| 华丽翡翠台 | 点播列表（非直播） |
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

## 本机判定不可达（节选）

| 频道 | 状态 | 地址 |
| --- | --- | --- |
| CCTV-16 | 返回非流内容 | `http://74.91.26.218:82/live/cctv16hd.m3u8` |
| CCTV4K真4K | 连接被拒 | `http://vip1.xinketongxun.fun:8082/tsfile/live/1026_1.m3u8` |
| 河南卫视 | 连接被拒 | `http://107.150.60.122/live/hawshd.m3u8` |
| 海南卫视 | HTTP 404 | `http://nn.7x9d.cn/地方台8563/海南.php?id=hnws` |
| 黑龙江卫视 | URLError | `https://idclive.hljtv.com:4430/live/hljws_own.m3u8` |
| 太谷新闻综合 | RemoteDisconnected | `https://p2.vzan.com/slowlive/596867413819827251/live.m3u8?zbid=1725814` |
| 汾西综合 | 连接超时 | `https://qmmqvzoz.live.sxmty.com/live/hls/f24f8a390c084386a564074c92601` |
| 黑龙江农业科教频道 | URLError | `https://idclive.hljtv.com:4430/live/hljgg_hd.m3u8` |
| 黑龙江文体 | URLError | `https://idclive.hljtv.com:4430/live/hljwy_hd.m3u8` |
| 黑龙江都市 | URLError | `https://idclive.hljtv.com:4430/live/dushi_hd.m3u8` |
| 绍兴电视台公共 | 连接超时 | `http://live.shaoxing.com.cn/video/s10001-sxtv2/index.m3u8?%E5%85%B3%E6` |
| 山东教育 | HTTP 404 | `https://test1.live.sdetv.com.cn/live/dianshizhibo/playlist.m3u8` |
| 新野综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/11329-1.m3u8` |
| 永城综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/11481-1.m3u8` |
| 荥阳综合 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://tvpull.dxhmt.cn:9081/tv/10182-1.m3u8` |
| 海南公共 | HTTP 404 | `http://nn.7x9d.cn/地方台8563/海南.php?id=ggpd` |
| 海南少儿 | HTTP 404 | `http://nn.7x9d.cn/地方台8563/海南.php?id=sepd` |
| 海南文旅 | HTTP 404 | `http://nn.7x9d.cn/地方台8563/海南.php?id=wlpd` |
| 海南新闻 | HTTP 404 | `http://nn.7x9d.cn/地方台8563/海南.php?id=xwpd` |
| 海南自贸 | HTTP 404 | `http://nn.7x9d.cn/地方台8563/海南.php?id=jjpd` |
| 剑阁综合 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel105549/pla` |
| 广元公共 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel101257/pla` |
| 广元综合 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel100999/pla` |
| 旺苍新闻综合 | URLError | `http://channel.wcrmt.cn:80/nmip-media/channellive/channel105268/playli` |
| 朝天综合 | 连接超时 | `https://m3u8.channel.dzsm.com/nmip-media/channellive/channel104601/pla` |
| 易门综合 | 连接超时 | `https://zb-live.ynurl.com/yimen/3b75a2f9-7941-46b7-992d-a9796fbca5fe.m` |
| 通海电视台 | 连接超时 | `https://zb-live.ynurl.com/tonghai/3bfe3a9e-48e6-4c1e-8770-1df66447cc6c` |
| 宁夏公共 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://hls.ningxiahuangheyun.com/live/nxgg1M.m3u8` |
| 宁夏文旅 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://hls.ningxiahuangheyun.com/live/nxwl1M.m3u8` |
| LIVE三立 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/setnewsrtmp/playlist.m3u8` |
| TVBS新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/tvbsnewsqt/playlist.m3u8` |
| 三立新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/iNEWS/playlist.m3u8` |
| 东森新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/EBCNews/playlist.m3u8` |
| 中天新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/CtiNEWS1/playlist.m3u8` |
| 中视新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/ctvnewsqt/playlist.m3u8` |
| 华丽翡翠台(新加坡) | 连接超时 | `http://cdn3.123.rr.kg/stream/live/jade/` |
| 华视新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/ctsnewsqt/playlist.m3u8` |
| 民视新闻 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://d2jc41c1shgcol.cloudfront.net/live/ftvnewsqt/playlist.m3u8` |
| 纬来体育 | 复核仍失败（HTTP 403（限流/地区限制）） | `https://hlsz.yjjcfw.com/live/vl.m3u8?expire=1786948372&sign=2e4a56b89f` |
| 香港卫视 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://webcast.hkstv.tv/livestream/mutfysrq/playlist.m3u8` |
| 凤凰中文 | 连接超时 | `http://zmgd.zyrnet.com:8888/hls/110/index.m3u8` |
| 凤凰资讯 | 连接超时 | `http://zmgd.zyrnet.com:8888/hls/109/index.m3u8` |
| Golf Channel (United States) (576p) | HTTP 404 | `https://tvsen6.aynaott.com/golfchannel/index.m3u8` |
| NewTV古装剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c58_fast_947_1080P_t10/c` |
| NewTV大家剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c58_fast_975_1080P_t10/c` |
| NewTV家庭剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c59_fast_999_1080P_t10/c` |
| NewTV泰语剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c58_fast_949_1080P_t10/c` |
| NewTV爱情剧场 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://lvbaiducdnct.inter.ptqy.gitv.tv/tslive/c59_fast_967_1080P_t10/c` |
| 美亚电影 | RemoteDisconnected | `http://iptv.4666888.xyz/iptv2A.php?id=30` |
| Jade | 连接超时 | `http://103.172.187.30:12000/stream/mytv/null-1/master.m3u8` |
| CCTV2 | 连接超时 | `http://101.35.240.114:88/live.php?id=CCTV2` |
| Asian Drama | 连接超时 | `http://103.172.187.30:12000/stream/mytv/null-11/master.m3u8` |
| Mei Ah Movie Channel | 连接超时 | `http://103.172.187.30:12000/stream/mytv/null-2/master.m3u8` |
| 五星体育 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://101.35.240.114:88/live.php?id=五星体育` |
| CCTV-5 | 连接超时 | `http://207.56.13.146:81/cdnlive/cctv5.m3u8` |
| CCTV-16 | 连接超时 | `http://207.56.13.146:81/cdnlive/cctv16.m3u8` |
| Arena Sport Premium M3 | 复核仍失败（HTTP 403（限流/地区限制）） | `http://telekomsrbije.com:2095/play/lhpjmkfVyhON1JAiZCx7vgvje3t-Jiqa5d9` |
| ESPN 2 Latin America Colombia (1080p) | 复核仍失败（HTTP 403（限流/地区限制）） | `http://190.61.47.54:8000/play/a005/index.m3u8` |
| ESPN Latin America Colombia (1080p) | 复核仍失败（HTTP 403（限流/地区限制）） | `http://190.61.47.54:8000/play/a004/index.m3u8` |
| Eurosport (720p) | HTTP 404 | `https://drk6xq0vhn.gpcdn.net/live/euro_sports_hd_abr/index.m3u8` |
| … | 另有 834 条 | |

## 移出订阅的原因

| 原因 | 条数 |
| --- | --- |
| 连接超时 | 222 |
| HTTP 404 | 152 |
| 连接被拒 | 124 |
| 复核仍失败（HTTP 403（限流/地区限制）） | 79 |
| TLS 握手失败 | 71 |
| URLError | 69 |
| 域名解析失败 | 51 |
| HTTP 500 | 42 |
| 返回非流内容 | 27 |
| HTTP 502 | 20 |
| HTTP 302 | 15 |
| HTTP 418 | 8 |
| HTTP 523 | 5 |
| RemoteDisconnected | 3 |
| HTTP 400 | 3 |

完整逐条清单见 `removed.tsv`（894 条）。
未通过校验但未判死的源另存于 `pending.m3u`，需要时可自行加回。

## 判定边界

报告只反映**跑清洗那台机器的网络**能连到什么，不是源站的最终状态。
403/429 里常混着出口 IP 限流或网络策略拦截——典型特征是 1ms 返回、空响应体、
没有 Server 头，TCP 甚至从未真正建连。这类不算源站判死，换个网络或播放器可能照样能播。
移出的条目都在 `removed.tsv` 留了完整地址和原始属性，确认某条其实能播时可直接加回。
