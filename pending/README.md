# pending/ 待确认源（已并入正式清单）

> **2026-11-10 已全部并入。** 这里的两份清单都写进了 `source/curated.m3u`，主订阅 `tv.m3u` 现为 346 条。本目录只留作追溯，不再有“待确认”含义。

这里的源都经过本机直连实测。播放器直接订阅根目录 `tv.m3u` 即可，不需要再单独导入 `pending.m3u`。

实测标准与正式清单一致：TCP 可建连 → 播放列表有效 → 追到分片 → 间隔 8~10 秒序列号前进。

## 凤凰卫视

现有正式清单里只有一条 `凤凰资讯 [FLV]`，是 FLV 流，部分播放器会卡。这次找到三条 HLS：

| 频道 | 地址 | 实测 |
| --- | --- | --- |
| 凤凰中文 | `http://173.208.234.146/live/fhzw.m3u8` | 200，序列号 48935→48936、48986→48988，两轮均前进 |
| 凤凰资讯 | `http://zmgd.zyrnet.com:8888/hls/109/index.m3u8` | 200，78ms，序列号 105902→105903、105990→105992 |
| 凤凰香港 | `http://122.152.202.33/s/81a8a44f/index.m3u8?id=fhhk` | 200，序列号 1794225638→1794225644、1794226090→1794226101 |

建议：确认后把 `tv.m3u` 里那条 FLV 换成 `zyrnet` 的凤凰资讯，同时补上凤凰中文、凤凰香港。三条都是第三方中转，不是凤凰官方 CDN，长期稳定性还要观察。

顺手排掉的：ifeng 官方 `play-flive.ifeng.com` 和 `playtv-live.ifeng.com` 的子列表全是 404；`tvfix.woodong.workers.dev` 在本机整体超时；抖音 CDN 那两条也超时；`218.206.193.218` 能拉到列表但序列号不动，判为循环回放。

## 电影频道

| 频道 | 地址 | 实测 |
| --- | --- | --- |
| CCTV第一剧场 | `http://38.75.136.137:98/gslb/dsdqpub/dyjc.m3u8?auth=testpub` | 两轮 36029→36030，稳定 |
| CCTV风云剧场 | `http://38.75.136.137:98/gslb/dsdqpub/fyjc.m3u8?auth=testpub` | 两轮 36031→36032，稳定 |
| CCTV怀旧剧场 | `http://38.75.136.137:98/gslb/dsdqpub/hjjc.m3u8?auth=testpub` | 两轮 36027→36028，稳定 |
| CHC高清电影 | `http://38.75.136.137:98/gslb/dsdqpub/chchd.m3u8?auth=testpub` | 首轮 164→165；第二轮 170→170 未动，更新周期偏长，建议多观察几次再定 |

`38.75.136.137` 这个 host 同时提供 CHC 动作、CHC 家庭影院等，正式清单里已有同名频道，所以这里只列正式清单没有的四个。`auth=testpub` 是公开测试参数，如果哪天失效，整组会一起挂。

## 埋堆堆

这次没有收录，本机环境确实走不通：

- `tv.iill.top/huya/*`、`48tv.cn` 代理域名全部超时
- 虎牙接口 `mp.huya.com` 能返回 `sStreamName` 和 `sHlsUrl`，但拼出来的直链一律 403，带 `Referer: huya.com` 也一样
- 直链自带 `wsSecret`、`wsTime` 鉴权，即使能播也会几小时过期，不适合写进静态订阅

如果换到能正常访问虎牙的网络，或者挂代理，可以再试代理域名那一批。埋堆堆本身是 TVB 港剧轮播，不是电影台，内容以剧集为主。

## 怎么合并

确认某条可用后：

1. 从 `pending.m3u` 复制对应两行
2. 粘到 `source/curated.m3u`，`group-title` 改成正式分组（`凤凰卫视` 或 `电影频道`）
3. 删掉 `pending.m3u` 里的那条
4. 跑 `python scripts/clean.py`，或直接等 Actions 下一轮

`pending/` 不在 `config.json` 的 `inputs` 里，不会被自动清洗，也不会进 `tv.m3u`。

## 外部列表核实（external-lists）

2026-11-09 对 8 个外部列表做了存活核实，结果单独放在 `external-lists.m3u` 和 `external-lists.md`。

- 拉不下来的：`iptv.yang-1989.xyz`（403）、`live.freetv.top/douyuyqk.m3u`（超时）、`goodiptv.club` 两个（连接被重置）
- 整站失效的：`aptv_ya`（5011 条）、`aptv_yqk`（811 条），抽样 119 条全部 404
- 可用的：`suxuang/myIPTV` 1225 条里 125 条可用；`iptv.445569.xyz` 抽样 1016 条里 142 条可用

去重后 245 个频道，新增 191 条写在 `external-lists.m3u`（不含 8 条直播房间）。
港澳台和电影频道补得最多：凤凰中文/资讯、TVB 系列、HOY、RTHK、澳视、天映、CHC、NewTV 剧场。

带 `txSecret`、`expire`、`sign` 的地址会过期，导入后如果失效属于正常。
