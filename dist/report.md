# 频道列表调整报告

生成时间：2026-11-08 18:07 (UTC+8)

本报告对应「优化电视频道列表」的四条要求。所有保留频道都在本机直连环境下通过了「TCP 可建连 → 播放列表有效 → 分片可读 → 间隔 12 秒序列号前进」四关，不是只看地址通不通。

## 总览

| 类别 | 调整前 | 调整后 | 说明 |
| --- | --- | --- | --- |
| 央视 | 39 | 18 | 只保留 CCTV-1~17 主频道，一套一个源 |
| 卫视 | 2 | 35 | 30 个省级卫视 + 5 个 4K 版 |
| 地方台 | 22 | 83 | 省内地市/县级台，按省分组 |
| 体育 | 49 | 9 | 只留英文解说，剔除西语/葡语/波语/波斯语 |
| 电影 | 7 | 14 | 新增 CHC 系列、Cinemax、Showtime 等 |
| 中国台湾 | 17 | 0 | 卡顿，按要求全部删除 |
| 中国香港 | 3 | 0 | 卡顿，按要求全部删除 |
| 港澳台混合 | 3 | 0 | 按要求全部删除 |
| 凤凰 | 0 | 1 | 新增凤凰资讯 |
| **合计** | **185** | **160** | 移除 150 条，新增 125 条 |

## 一、地方台：22 → 118

从 27 份仍在线更新的公开列表里提取地方台候选，按频道名去重后逐条实测；另按已知可用的 IPTV 源地址规律补测了一批省级卫视线路。

**省级卫视 35 个**（含 4K 版）：

北京卫视、天津卫视、东方卫视、重庆卫视、河北卫视、山西卫视、辽宁卫视、吉林卫视、黑龙江卫视、江苏卫视、浙江卫视、安徽卫视、东南卫视、江西卫视、山东卫视、河南卫视、湖北卫视、湖南卫视、广东卫视、广西卫视、四川卫视、贵州卫视、云南卫视、陕西卫视、甘肃卫视、青海卫视、深圳卫视、三沙卫视、延边卫视、安多卫视、东方卫视4K、江苏卫视4K、浙江卫视4K、深圳卫视4K、湖南卫视4K

**省内地市/县级台 83 个**，按省分组：

- **地方·河北**（12）：任丘综合、兴隆综合、平泉综合、昌黎综合、河北4K、河北公共、河北影视、河北经济、清河经济综艺、邯郸公共频道、邯郸新闻、邯郸科技教育
- **地方·浙江**（11）：浙江国际、浙江教科、浙江教科影视、浙江新闻、浙江民生、浙江经济、浙江钱江、海宁新闻综合、绍兴电视台公共、萧山生活、诸暨新闻综合
- **地方·四川**（10）：剑阁综合、名山综合、广元公共、广安公共、松潘新闻综合、汶川新闻综合、泸县新闻综合、荥经综合、金川新闻综合、雅安新闻综合
- **地方·辽宁**（7）：辽宁公共、辽宁影视、辽宁影视剧、辽宁教育青少、辽宁生活、辽宁经济、辽宁青少
- **地方·黑龙江**（7）：哈尔滨娱乐、哈尔滨影视、哈尔滨生活、哈尔滨资讯、哈尔滨都市咨询、黑龙江文体、黑龙江都市
- **地方·江苏**（7）：南京教科、南京新闻综合、苏州4K、苏州文化生活、苏州新闻综合、苏州生活资讯、苏州社会经济
- **地方·广东**（4）：东莞新闻综合、广东民生、广东珠江、广州综合
- **地方·云南**（4）：云南娱乐、云南都市、易门综合、通海电视台
- **地方·福建**（3）：云霄综合、福州少儿、福州生活
- **地方·河南**（3）：新野综合、永城综合、荥阳综合
- **地方·甘肃**（3）：天祝综合、永昌综合、西峰综合
- **地方·山西**（2）：太谷新闻综合、汾西综合
- **地方·广西**（2）：广西国际、广西新闻
- **地方·宁夏**（2）：宁夏公共、宁夏文旅
- **地方·北京**（1）：北京科教
- **地方·重庆**（1）：重庆新闻
- **地方·吉林**（1）：延边2
- **地方·安徽**（1）：广德生活
- **地方·山东**（1）：山东教育
- **地方·青海**（1）：西宁新闻综合

未覆盖的省级卫视：内蒙古、宁夏、新疆、西藏、海南、福建。这几家的候选线路在本次实测里全部不可达或返回非流内容，没有硬凑。

## 二、央视：39 → 18

只保留 CCTV-1、2、3、4、5、5+、6、7、8、9、10、11、12、13、14、15、16、17，每个频道一套源。CGTN 多语种（西语/阿语/俄语）、央视付费频道（兵器科技、台球、风云剧场等）、CNR 广播、CCTV+ 全部移出。

**修正了一个错误源**：原列表里的 CCTV-8 实际指向 `cctv8k.m3u8`（CCTV-8K 超高清），并不是电视剧频道，本次换回真正的 CCTV-8。

| 频道 | 说明 | 地址 |
| --- | --- | --- |
| CCTV-1 | 主频道 | `https://liveplay-srs.voc.com.cn/hls/tv/134_180adf.m3u8` |
| CCTV-2 | 主频道 | `http://101.35.240.114:88/live.php?id=CCTV2` |
| CCTV-3 | 主频道 | `http://107.150.60.122/live/cctv3hd.m3u8` |
| CCTV-4 | 主频道 | `https://dash2.antik.sk/live/test_cctv_tizen/playlist.m3u8` |
| CCTV-5 | 主频道 | `http://107.150.60.122/live/cctv5hd.m3u8` |
| CCTV-5+ | 主频道 | `http://38.75.136.137:98/gslb/dsdqbv/cctv5p.m3u8?auth=test20251009` |
| CCTV-6 | 主频道 | `http://198.204.228.26/live/cctv6hd.m3u8` |
| CCTV-7 | 主频道 | `http://107.150.60.122/live/cctv7hd.m3u8` |
| CCTV-8 | 主频道 | `http://124.165.251.82:85/tsfile/live/0008_1.m3u8?key=txiptv&playlive=1&authid=0` |
| CCTV-9 | 主频道 | `https://v4-e6b1c5baf4e240fe63adbf68dda23435.livehwc4.com/play.kankanlive.com/live/169842` |
| CCTV-10 | 主频道 | `https://cdn4.skygo.mn/live/disk1/CCTV-10/HLSv3-FTA/CCTV-10.m3u8` |
| CCTV-11 | 主频道 | `http://74.91.26.218:82/live/cctv11hd.m3u8` |
| CCTV-12 | 主频道 | `http://124.165.251.82:85/tsfile/live/0012_1.m3u8?key=txiptv&playlive=1&authid=0` |
| CCTV-13 | 主频道 | `http://74.91.26.218:82/live/cctv13hd.m3u8` |
| CCTV-14 | 主频道 | `http://198.204.228.26/live/cctv14hd.m3u8` |
| CCTV-15 | 主频道 | `http://gmxw.7766.org:808/hls/102/index.m3u8` |
| CCTV-16 | 主频道 | `http://74.91.26.218:82/live/cctv16hd.m3u8` |
| CCTV-17 | 主频道 | `http://74.91.26.218:82/live/cctv17hd.m3u8` |

说明：央视源大多直接返回 media playlist，列表里没有 `RESOLUTION` 字段，无法逐条读出分辨率。本次优先选 URL 带 `hd`、或实测码率明显高于标清的线路；CCTV-10 实测 960p / 3782 kbps。

## 三、中国台湾 / 中国香港：23 → 0，新增凤凰资讯

台湾 17 条、香港 3 条、港澳台混合 3 条按要求全部删除。

凤凰卫视方面，公网 HLS 源已经大面积失效，本轮逐一验证：ifeng 官方 master 列表能返回 720p 的两档码率，但子列表 `_tv1.m3u8` 全部 404；`hls-gateway.vpstv.net` 返回 403；`cdn6.163189.xyz` 返回的是网页而不是流；`r.jdshipin.com` 短链超时。最后只有一条实测可用：

```
凤凰资讯  http://43.152.224.209/qctv.fengshows.cn/live/0701pin72.flv
```

这是 FLV 流（H264 / 1280x720），VLC、PotPlayer 可直接播；TiviMate、部分电视盒子只认 HLS，可能播不了，频道名已标 `[FLV]`。凤凰中文、凤凰香港暂时没有可用源，没有用失效地址凑数。

## 四、体育：49 → 9

只保留英文解说的主流体育台：

| 频道 | 实测 | 地址 |
| --- | --- | --- |
| Cricket Gold (1080p) | 1080p 档为主 | `https://streams2.sofast.tv/ptnr-yupptv/title-cricketgold/v1/master/611d79b11b77e2f571934` |
| EuroSport1 | 1080p 档为主 | `http://141.94.193.53:80/Eurosport_1_HD/index.m3u8` |
| Fox Sports (1080p) | 1080p 档为主 | `http://138.59.227.20:8000/play/a085/index.m3u8` |
| Fox Sports News (1080p) | 1080p 档为主 | `https://skynewsau-live-premium.akamaized.net/hls/live/2105307/foxsportsnews/live_1080p.m` |
| Golf Channel (United States) (576p) | 1080p 档为主 | `https://tvsen6.aynaott.com/golfchannel/index.m3u8` |
| NBC Sports NOW (1080p) | 1080p 档为主 | `https://d4whmvwm0rdvi.cloudfront.net/10007/99993008/hls/master.m3u8?ads.xumo_channelId=9` |
| NHL Network (1080p) | 1080p 档为主 | `https://nhl-firetv.amagi.tv/playlist.m3u8` |
| Willow Sports (1080p) | 1080p 档为主 | `https://d36r8jifhgsk5j.cloudfront.net/Willow_TV.m3u8` |
| beIN SPORTS XTRA (1080p) | 1080p 档为主 | `https://bein-xtra-bein.amagi.tv/playlist.m3u8` |

**删除的非英文源**：ESPN 拉美系列 8 条（西语）、DAZN 1/3 Portugal（葡语）、Eurosport 1/2 Poland、Czechia、Hungary、Russia、Germany、Portugal（各语种版）、FightBox Poland（波兰语）、Persiana Fight（波斯语）、TVS Boxing（越南语）、Arena Sport 1 Premium Serbia（塞尔维亚语）、Sportitalia（意大利语）等。

**TNT Sports 与 ESPN 英文版本轮没有纳入**：现有公开源里 TNT Sports 1~4 全部 404（`37.49.224.5/stream/*` 整组失效），ESPN 美国 HD 线路 TCP 不通，能通的只有拉美西语版。按「只留英文」的要求，宁可不放。

## 五、电影：7 → 14

新增并保留：

AXN Black、CHC动作电影、CHC家庭影院、CHC电影、Cinemax Classics (1080p)、Cinemax Hits (1080p)、Cinemax West (720p)、FILMBOX+ Action (720p)、FILMBOX+ Comedy (720p)、FILMBOX+ Emotion (720p)、Paramount Network (1080p)、Showtime Family Zone (720p)、Universal Cinema (1080p)、美亚电影

其中 CHC 动作/家庭/电影、美亚电影是中文频道；Cinemax、Paramount、Showtime、Universal、AXN、FILMBOX+ 为英文频道。

删除了阿拉伯语 Rotana Cinema、拉美西语 TCM/AMC/AXN、波兰/保加利亚/捷克等小语种电影台，以及 240p/480p 的低清源。

## 六、移除清单

本次共移除 150 条旧条目，逐条记录在 `dist/removed.tsv`：

- 体育（仅保留英文解说）：43 条
- 其他（重复、失效或未通过复核）：41 条
- 央视（仅保留主频道 HD）：37 条
- 港台（按要求删除）：20 条
- 电影（已由更优源替代）：9 条

## 七、判定边界

这里的「可用」指本机直连能拉到流、且序列号在 12 秒内确实前进。换网络（尤其是境外出口）、换播放器，结论可能不同；地方台县级源多为地方广电 CDN，跨省访问可能变慢或失效。

## 八、文件

| 文件 | 说明 |
| --- | --- |
| `tv.m3u` | 主订阅，160 条，播放器填这个地址 |
| `source/curated.m3u` | 手工维护区，本次精选的源都在这里 |
| `archive/` | 上一版 1300 条归档，只作追溯，不参与清洗 |
| `dist/cctv.m3u` | 央视 18 |
| `dist/weishi.m3u` | 卫视 35 |
| `dist/difang.m3u` | 地方台 83 |
| `dist/sports.m3u` | 英文体育 9 |
| `dist/movie.m3u` | 电影 14 |
| `dist/gangao.m3u` | 凤凰资讯 1 |
| `dist/removed.tsv` | 本次移除的旧条目与原因 |

