# 直播源清洗报告

生成时间：2026-11-07 15:20 (UTC+8)

| 指标 | 数值 |
| --- | --- |
| 原始条目 | 1212 |
| 实测通过 | 79 |
| 未通过校验（已移出订阅） | 24 |
| 本机判定不可达 | 1109 |
| 写入订阅 | 79 |
| 有效频道数 | 78 |
| 平均响应 | 643 ms |

## 未通过校验（已移出订阅）

| 频道 | 原因 |
| --- | --- |
| 民视 | 非 http(s) 协议（rtmp） |
| 台视 | 非 http(s) 协议（rtmp） |
| 中视 | 非 http(s) 协议（rtmp） |
| 华视 | 非 http(s) 协议（rtmp） |
| 非凡新闻 | 非 http(s) 协议（rtmp） |
| 东森超视 | 非 http(s) 协议（rtmp） |
| MOMO TV | 非 http(s) 协议（rtmp） |
| 纬来日本 | 非 http(s) 协议（rtmp） |
| 纬来体育 | 非 http(s) 协议（rtmp） |
| 纬来育乐 | 非 http(s) 协议（rtmp） |
| DAZN体育1 | 非 http(s) 协议（rtmp） |
| DAZN体育2 | 非 http(s) 协议（rtmp） |
| 精灵宝可梦 | 点播列表（非直播） |
| 亮剑 | 点播列表（非直播） |
| 特种兵之火凤凰 | 点播列表（非直播） |
| 使徒行者 | 点播列表（非直播） |
| 沐川综合 | 非 http(s) 协议（rtmp） |
| 石棉综合 | 非 http(s) 协议（rtmp） |
| 邢台生活 | 播放列表停滞（循环回放） |
| 1987年春晚 | 播放列表停滞（循环回放） |
| 1988年春晚 | 播放列表停滞（循环回放） |
| 1989年春晚 | 播放列表停滞（循环回放） |
| 2024年春晚 | 播放列表停滞（循环回放） |
| 2025年春晚 4K | 播放列表停滞（循环回放） |

## 本机判定不可达（节选）

| 频道 | 状态 | 地址 |
| --- | --- | --- |
| 拆弹专家1 | ConnectionAbortedError | `https://vip.ffzy-online.com/20221015/719_80ff87c2/index.m3u8` |
| 北京卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://139.ye23.vip/dl/btv2502.php?id=bjws4` |
| 东方卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://bp-resource-dfl.bestv.cn/148/3/video.m3u8` |
| 湖南卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=湖南卫视4K` |
| 浙江卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://ali-xwl.cztv.com/live/channel4k2160p.m3u8` |
| 江苏卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://8.138.7.223/tv/jsws4k.php` |
| 广东卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=广东卫视4K` |
| 深圳卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://nn.7x9d.cn/深圳最新.php?id=szws4k` |
| 山东卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=山东卫视4K` |
| 四川卫视4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=四川卫视4K` |
| CCTV4K真4K | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://vip1.xinketongxun.fun:8082/tsfile/live/1026_1.m3u8` |
| 河北卫视 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://event.pull.hebtv.com/jishi/weishi_tingyun.m3u8` |
| CCTV1 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV1` |
| CCTV2 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://148.135.93.213/live.php?id=CCTV2` |
| CCTV3 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV3` |
| CCTV4 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://148.135.93.213/live.php?id=CCTV4` |
| CCTV5 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV5` |
| CCTV5+ | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://148.135.93.213/live.php?id=CCTV5p` |
| CCTV6 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV6` |
| CCTV7 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://148.135.93.213/live.php?id=CCTV7` |
| CCTV8 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV8` |
| CCTV9 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://148.135.93.213/live.php?id=CCTV9` |
| CCTV10 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV10` |
| CCTV11 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://148.135.93.213/live.php?id=CCTV11` |
| CCTV12 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV12` |
| CCTV13 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://148.135.93.213/live.php?id=CCTV13` |
| CCTV14 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV14` |
| CCTV15 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://148.135.93.213/live.php?id=CCTV15` |
| CCTV16 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://101.35.240.114:88/live.php?id=CCTV16` |
| CCTV17 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://74.48.192.96:82/live.php?id=CCTV17` |
| CCTV-兵器科技 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.98:5140` |
| CCTV-世界地理 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.93:5140` |
| CCTV-风云足球 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.96:5140` |
| CCTV-风云音乐 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.87:5140` |
| CCTV-风云剧场 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.89:5140` |
| CCTV-第一剧场 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.86:5140` |
| CCTV-怀旧剧场 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.90:5140` |
| CCTV-文化精品 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.81:5140` |
| CCTV-女性时尚 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.94:5140` |
| CCTV-卫生健康 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://nas.hssvm.com:8888/udp/225.1.1.210:5002` |
| CCTV-央视台球 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.80:5140` |
| CCTV-央视高网 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.95:5140` |
| CCTV-电视指南 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.97:5140` |
| 中国天气 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://hls.weathertv.cn/tslslive/qCFIfHB/hls/live_sd.m3u8` |
| 中国交通 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://drive.mxmy.net:8888/udp/239.3.1.188:8001` |
| 直播中国 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `https://gcalic.v.myalicdn.com/gc/wgw05_1/index.m3u8?contentid=28201805` |
| CETV-1 综合教育 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.220.198:5140` |
| CETV-2 空中课堂 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://www.lizhinas.top:1009/rtp/239.252.219.73:5140` |
| CETV-3 教育服务 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://rrs01.hw.gmcc.net:8088/PLTV/81/224/3221226722/1.m3u8` |
| CETV-4 职业教育 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://rrs01.hw.gmcc.net:8088/PLTV/81/224/3221226724/1.m3u8` |
| CGTN英语 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://english-livetx.cgtn.com/hls/yypdyyctzb_hd.m3u8` |
| CGTN俄语 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://russian-livews.cgtn.com/hls/LSvexABhNipibK5KRuUkvHZ7220802LSTez` |
| CGTN法语 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://espanol-liveali.cgtn.com/hls/LSveOGBaBw41Ea7ukkVAUdKQ220802LSTe` |
| CCTV1 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://iptv.huuc.edu.cn/hls/cctv1hd.m3u8` |
| CCTV2 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://iptv.huuc.edu.cn/hls/cctv2hd.m3u8` |
| CCTV3 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://iptv.huuc.edu.cn/hls/cctv3hd.m3u8` |
| CCTV4 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://iptv.huuc.edu.cn/hls/cctv4hd.m3u8` |
| CCTV5 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://iptv.huuc.edu.cn/hls/cctv5hd.m3u8` |
| CCTV6 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://iptv.huuc.edu.cn/hls/cctv6hd.m3u8` |
| CCTV7 | 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | `http://iptv.huuc.edu.cn/hls/cctv7hd.m3u8` |
| … | 另有 1049 条 | |

## 移出订阅的原因

| 原因 | 条数 |
| --- | --- |
| 多轮批量核实均未通过（可能受出口限流影响，见 removed.tsv） | 1108 |
| 非 http(s) 协议（rtmp） | 14 |
| 播放列表停滞（循环回放） | 6 |
| 点播列表（非直播） | 4 |
| ConnectionAbortedError | 1 |

完整逐条清单见 `removed.tsv`（1133 条）。
未通过校验但未判死的源另存于 `pending.m3u`，需要时可自行加回。

## 交叉验证（2026-11-07 17:02 UTC+8）

终审之后另跑了一轮**单并发、串行、短超时**抽查，只取播放列表头部，不追分片，
避免高并发再次把出口 IP 打进限流。样本 38 条：

| 样本 | 条数 | 能拉到 m3u8 | 403/429 | 404 / TLS / 其他 |
| --- | --- | --- | --- | --- |
| 写入订阅的 79 条里抽 | 18 | **18** | 0 | 0 |
| `removed.tsv` 里抽 | 20 | **0** | 15 | 5 |

保留源 18/18 全部返回 200 且是有效播放列表，被移出的源 20/20 无一可拉流。
终审结果稳定，不需要回滚。抽查逐条结果见 `dist/crosscheck.tsv`（本次快照，不随每日清洗更新）。

## 判定边界

上面 1108 条「多轮批量核实均未通过」里，**大部分不是源站把频道关了**。
单独复查那批 403 发现：响应 1ms 返回、响应体为空、没有 Server 头，
部分连 TCP 都没建连成功，HTTP 层却直接给 403。这是本机网络中间层拦截／出口策略，
不是源站拒绝。CCTV 全系、CGTN、各卫视 4K 整批消失，主要就是这个原因。

所以这份报告只说明**跑清洗那台机器连不到什么**，不代表频道在别处也播不了。
换个网络、用播放器或电视盒子打开，其中一些大概率还能看。
`removed.tsv` 保留了每一条的完整地址和原始 UA／Referer 属性，
确认某条其实能播时，把它抄回 `source/tv.m3u` 即可，主源归档 1287 条也一直没动。
