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

上表是 15:20 那次全量清洗的快照。晚间先后做过三轮补充：
先是**央视 / 港台专项复核**，从原始归档和公开源补回 13 条（79 → 92）；
随后按「不要再用旧源、在线找新的」重新做了一轮**在线新源专项**，
又补入 44 条（92 → 136）；最后按「要 NBA 和格斗」做了**体育频道专项**，
再补 49 条（136 → **185**）。根目录 `tv.m3u` 当前 185 条，
分类文件（新增 `sports.m3u`）、`dist/all.m3u`、`detail.tsv` 已同步。
央视港台专用 62 条、在线新增 44 条、体育专用 49 条都已是主订阅的子集，
不存在只留在专用文件里、没进主订阅的地址。三轮详见文末专章。

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
确认某条其实能播时，把它抄回 `source/tv.m3u` 即可。主源归档原有 1287 条一条没删，
晚间在末尾追加了 13 条专项复核通过的线路，现在是 1300 条。

## 央视 / 中国香港 / 中国台湾专项复核（2026-11-07 晚间）

上一轮「失败就删」把三类频道整批移出了订阅，这次单独把它们捞回来重测。

**候选池 617 条**：原始归档 329 条、Guovin 188 条、iptv-org 的 cn/hk/tw 共 100 条。
判定口径和主清洗一致——TCP 预筛、拿播放列表头、追到分片真读到数据，
再隔 15～35 秒抓第二遍列表，媒体序列号不前进的判循环回放。
多轮结果按 URL 合并去重，同一频道最多留 3 条线路。

| 结果 | 条数 |
| --- | --- |
| 多轮合并后实测通过 | 17（央视 12 / 中国台湾 4 / 中国香港 1） |
| 其中新并入主订阅 | 13（另 4 条订阅里已有） |
| 专用订阅 `dist/cctv-hk-tw.m3u` | 18（央视 13 / 中国香港 1 / 中国台湾 4） |
| 归档候选恢复包 `dist/three-archive.m3u` | 278（230 个频道，标注未验证） |

央视补回的是 CCTV-1/9/10、CGTN 系列和熊猫直播；中国台湾补回
Beautiful Life TV、CGNTV Chinese、Taiwan Indigenous TV、唯心電視；
中国香港实测可用的只有**耀才财经台**，200 响应、326 ms、序列号正常推进。

### 香港源为什么只剩一条

这不是脚本误杀，是本机的网络边界。160 条香港候选的逐条判定存于
`dist/hk-probe.tsv`（含状态、HTTP 码、响应耗时、归因），分布是：

| 现象 | 条数 | 性质 |
| --- | --- | --- |
| 1 ms 空 403 | 93 | 本机网络中间层拦截，`r.jdshipin.com`、`163189.xyz` 等中转短链整批中招 |
| 真实 403 / 418 | 12 | 源站地区限制或反盗链（约 1～2 秒返回，与前一类不同） |
| TCP 未建连、TLS 握手失败 | 42 | 跨境链路不通 |
| 拿到列表但不合格 | 3 | 点播列表 / 无信号占位流 |

RTHK 港台电视 31/32、HOY TV 这些官方 HLS 都带 Geo-blocked 标记，
本机拿 403，换境外出口再试同样是 Akamai 的 Access Denied。
`epg.pw` 那条「凤凰香港」返回 200，但 master 指向的是
`nosignal_h264/playlist.m3u8`——无信号占位画面，不是真频道，没写进订阅。

因此香港频道以**候选恢复包**的形式单独交付：从原始归档里按频道名归类，
保留原始 UA／Referer，每个频道最多留 2 条线路，只保留 http/https，
频道名前统一加 `[未验证]`。它不进主订阅，避免把连不通的地址混回干净列表。
换网络、用播放器或挂代理时可以直接试这批地址，能播的再抄回 `source/tv.m3u`。

| 候选包分组 | 条数 |
| --- | --- |
| 候选·中国香港（未验证） | 87 |
| 候选·中国台湾（未验证） | 32 |
| 候选·中国澳门（未验证） | 8 |
| 候选·央视（未验证） | 151 |

**这份报告里的「可用」始终是指跑清洗这台机器能拉到流。**
香港这批源在别的网络下很可能正常，反之亦然。

## 在线新源专项（2026-11-07 晚间，第二轮）

上一节仍是围着旧归档复核。这一轮按「不要在原有的源里做验证，在线找其他可用的」重做：
`source/tv.m3u` 一条没读、一条没改，候选全部来自新拉取的在线公开列表。

**拉取**：搜索得到 29 个仍在自动更新的公开源，成功取回 22 个（1.86 MB 原始文本）。
主力是 bestK/iptv（每小时检测）、MercuryZz/IPTVN 港澳台专题、
epg.pw 的 hk/tw/cn 分地区列表、live.zbds.top 聚合、YueChan/Live、Kimentanm/aptv、
iptv-org 网站版 cn/hk/tw、Free-TV/IPTV 等。
7 个失败（Moexin、suxuang、dongyubin、vbskycn、hujingguang、iill 等），
原因多为仓库路径已变或域名不通，逐条记在 `dist/online-sources.tsv`。

**候选与判定**：只从这 22 份新列表里提取三类频道，并排除主订阅已有的 92 个地址，
得到 786 条全新候选。判定口径与前面一致。

| 阶段 | 条数 |
| --- | --- |
| 全新候选 | 786（央视 303 / 香港 243 / 台湾 240） |
| TCP 预筛：191 个 host，可建连 109 | 进入 HTTP 复核 284 |
| 列表头判定 | OK 147、DEAD 76、SOFT 42、BAD 19 |
| 两轮活性指纹 | 活跃 67、循环回放 33、列表无分片 46、点播 1 |
| 严格归类清洗后 | 48 |
| 排除与旧归档撞车 6 条、香港补测 +2 | **最终新增 44** |

**归类清洗**：`freetv`、`bigbig` 是国际聚合源，按短关键词归类会把
AlphaTV（希腊）、Knesset（以色列）、RadioItaliaTV（意大利）、
KCTV 광주（韩国）、UCTV（美国）等 16 条外国台误判成港台；
TVBS 也因为名字含 `tvb` 被算到香港。改成明确品牌词白名单重新判定，
并把判定顺序调成台湾 → 香港 → 央视，剔掉那 16 条，再按频道压到 2 条线路。

**香港补测**：243 条香港候选里 153 条跨境 TCP 未建连、7 条 RTHK 系真实地区限制 403。
把「拿到列表但追分片超时」的凤凰中文／资讯、翡翠台短链等 61 条挑出来，
用 6 秒超时补测，9 条拿到有效列表、2 条活性通过
（Asian Drama、Mei Ah Movie Channel，与 Jade 同一组 CDN）。
其余跨境未建连的不再重复耗时间。

**最终 44 条**：央视 28、中国台湾 13、中国香港 3。
主订阅 92 → 136，专用订阅 `dist/cctv-hk-tw.m3u` 18 → 62，
新增独立订阅 `dist/online-new.m3u` 44 条，持久化到 `source/online-new.m3u`
（与 1300 条旧归档分文件存放，互不影响）。
6 条与旧归档地址完全相同的按「不用旧源」要求剔除，其中含 CGTN 英语／法语、
台视新闻、美亚电影等，虽实测活跃但未纳入。

逐条判定见 `dist/online-probe.tsv`（786 条），源清单见 `dist/online-sources.tsv`。
判定边界与前面相同：这批「可用」也只是本机直连的结论。

## 体育频道专项：NBA / 格斗（2026-11-07 夜间，第三轮）

需求是要能看 NBA 和格斗。候选同样**全部来自在线公开列表**，
`source/tv.m3u` 旧归档一条没读、一条没改，已在订阅里的地址也全部排除。

**拉取**：新取 5 份列表 —— iptv-org 网站版 `categories/sports.m3u`（479 条）、
iptv-org 的 `us` / `uk` / `tw` 分区列表、Guovin/iptv-api 每日结果；
加上第二轮缓存的 22 份在线列表，共 27 份。3 个地址返回 404（bestK live.m3u
路径变更、epg.pw sports 分类不存在、AIPTV sports.m3u 已失效），
逐条记在 `dist/sports-sources.tsv`。

**归类**：只按频道名判定，不用分组兜底；英文短词一律走词边界。
这样避开了 `pinball` 里藏 `nba`、`Drammatico` 里藏 `mma`、
`atv` 藏在 `AlphaTV` 里这一串误判；「动物搏击赛」「游戏赛事」「咪咕直播-N」
轮播频道、足球／高尔夫／垂钓等与需求无关的也一并排除。
每个频道最多保留 2 条不同 host 的线路。

| 阶段 | 条数 |
| --- | --- |
| 全新候选 | 182（赛事台 149 / 格斗 27 / 篮球 6） |
| TCP 预筛：86 个 host，可建连 67 | HTTP 复核 121 |
| 列表头 | OK 70、DEAD 29、SOFT 21、BAD 1（另有 61 条 TCP 未建连） |
| 两轮活性指纹（间隔 20 秒） | 活跃 48、列表无分片 17、循环回放 4、点播 1 |
| 长超时补测（6 秒、追 variant、间隔 15 秒） | 13 条拿到列表、再活跃 5 条 |
| 合并去重 50 条，剔误判 His Glory TV 1 条 | **最终新增 49** |

**结果**：主订阅 136 → 185；`dist/sports.m3u` 49 条，分
`体育·NBA` 1 条（NBA TV 720p）、`体育·格斗` 7 条
（FightBox / FightBox HD / FightBox Poland、DAZN 3 Portugal、MMA-TV.com、
Persiana Fight、TVS Boxing）、`体育·赛事台` 41 条
（CCTV-5 / 5+ / 16、五星体育、广东体育、山东体育、天津体育、
ESPN 系列、TNT Sports、beIN SPORTS XTRA、Eurosport、Eleven Sports、
Arena Sport、M4 Sport、MNB Sport 等）。
持久化到 `source/sports.m3u`，配置里新增 `sports.m3u` 分类并置于匹配顺序首位，
避免 CCTV-5 被「CCTV」关键词优先归进央视频道分类。

格斗类里 21 条在首轮被判「列表无分片」或「限流」，
补测追 variant 后捞回 TVS Boxing；Pluto / jmp2.uk 那批
（PFL MMA、Bellator MMA、DAZN Combat、TNA Wrestling）两次都拿不到分片或
序列号不前进，按循环回放剔除，没有写进订阅。
`bigbig.m3u` 的「UFC」虎牙转播地址返回真实 404，也没有纳入。

**顺带修了一个通用解析 bug**：`#EXTINF` 属性里的 `http-user-agent` 常含逗号
（`(KHTML, like Gecko)`），`parse_m3u()` 原来按第一个逗号切分，
会把 UA 后半截当成频道名，产出 20 多条 `Chrome/149.0.0.0 Safari/...` 乱码。
现在按**引号外的第一个逗号**切分属性区与频道名，UA 属性本身照常保留并参与探测。
修复已落在仓库内的 `scripts/clean.py`，本地与 CI 用的是同一份。

逐条判定见 `dist/sports-probe.tsv`（182 条）。
判定边界不变：这些「可用」只说明本机直连能拉到流、且序列号在前进，
不保证频道内容或换网络后依然可播；赛事台播不播 NBA / UFC 要看当日节目表。
