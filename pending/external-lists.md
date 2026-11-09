# 外部列表存活核实（2026-11-09）

对 8 个列表逐个拉取、逐条实测（TCP → 列表头 → 两轮序列号）。带 UA/Referer 重试仍失败的列表单独说明。

## 列表状态

| 列表 | 拉取 | 实测条数 | 可用 | 存活率 |
| --- | --- | --- | --- | --- |
| suxuang（gh.aptv.app 代理） | 成功 1225 条 | 1202 | 125 | 10.4% |
| 445569 live.m3u | 成功 2460 条，传统频道 918 + 抽样 98 | 1016 | 142 | 14.0% |
| aptv_ya（虎牙） | 成功 5011 条，抽样 60 | 60 | 0 | 0.0% |
| aptv_yqk（虎牙） | 成功 811 条，抽样 59 | 59 | 0 | 0.0% |
| yang1989 playlist.m3u | 403，带 UA/Referer 仍 403 | - | - | - |
| freetv_douyu | 超时 | - | - | - |
| goodiptv 两个 | 连接被重置 | - | - | - |

## 去重后

可用原始 267 条，按频道名去重后 **245 条**，其中 199 条不在正式清单里（含 8 条直播房间，实际写入 `external-lists.m3u` 的是 191 条）。

| 分类 | 条数 |
| --- | --- |
| 央视 | 12 |
| 卫视 | 12 |
| 地方 | 41 |
| 港澳台 | 53 |
| 电影剧场 | 21 |
| 体育 | 13 |
| 海外 | 30 |
| 其他 | 55 |
| 直播房间 | 8 |

## 值得注意的频道

- 港澳台：凤凰中文/资讯、TVB1/TVBJ1/TVB星河/TVB Plus、明珠台、无线新闻、HOY TV/HOY资讯、RTHK31/32、ViuTVsix、澳视澳门/卫星、台视/中视/华视/东森/中天/三立/民视/TVBS 新闻、天映、Astro
- 央视：CCTV4K、CCTV5+、CGTN 英/西/法/阿/纪录、CEC 四个频道
- 卫视：东方/江苏/浙江/湖南 4K、河北、内蒙古、宁夏、海南、三沙、延边、农林
- 电影：CHC 动作/家庭/影迷、NewTV 五个剧场、天映系列、美亚C+、湖南电影、华数动作影院
- 体育：NBC Sports、NHL、Bein Sports Extra 2、Cricket Gold、辽宁体育
- 海外：RT 全系、ABC/CBC/CNA/Newsmax、PBS Kids、DLTV 泰语、Stara 印尼、Arirang、韩国 EBS

## 注意

- 带 `txSecret`、`expire`、`sign` 的 URL 有时效，几小时后可能失效，导入后要留意
- `cdn3/cdn6/cdn10.123.rr.kg`、`cdn3.indevs.in` 是第三方中转，稳定性一般
- 直播房间 8 条（Twitch/酷狗/抖音）单列，没有写进 `external-lists.m3u`
- 新增的 191 条在 `pending/external-lists.m3u`，确认后再并入 `source/curated.m3u`
