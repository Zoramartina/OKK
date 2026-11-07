# OKK 自用源

本地跑清洗时会把实测失败的源从订阅里删掉；GitHub Actions 每天凌晨跑一遍保守校验，只更新报告和分类，不覆盖订阅。手工维护的部分放在 `source/`，根目录的 `tv.m3u` 是机器生成的，别手改。

**根目录 `tv.m3u` 是唯一完整订阅**：央视港台专用、在线新增、体育专用这几份都只是它的子集视图，内容已经全部并入主订阅，播放器只填根目录这一份就能看全。

## 订阅地址

```
https://raw.githubusercontent.com/Zoramartina/OKK/main/tv.m3u
```

raw 直连不稳的话套镜像：

```
https://gh-proxy.com/https://raw.githubusercontent.com/Zoramartina/OKK/main/tv.m3u
```

## 目录

| 路径 | 说明 |
| --- | --- |
| `source/` | **手工维护区**，改了这里才算数 |
| `config.json` / `verify_config.json` / `recheck_config.json` | 常态配置 / 全量核实配置 / 低速补核配置 |
| `tv.m3u` | 生成物，只含实测通过的主源，订阅用的就是它，**185 条** |
| `dist/all.m3u` | 主源 + 自动搜集的合并版 |
| `dist/*.m3u`（分类） | `cctv` / `weishi` / `gangao` / `difang` / `sports` / `other` 六份分类版 |
| `dist/report.md` | 本次报告：剔了多少、为什么剔，附交叉验证结论 |
| `dist/crosscheck.tsv` | 2026-11-07 抽查快照，38 条逐条结果（不随每日清洗更新） |
| `dist/detail.tsv` | 全量逐条明细，含响应时间、速度、判定原因 |
| `dist/removed.tsv` | **从订阅移出的完整清单**，想找回某条源来这里翻 |
| `dist/pending.m3u` | 未通过校验但没判死的源（IPv6、rtmp、加密流、分片反盗链），可自行加回 |
| `dist/cctv-hk-tw.m3u` | **央视 / 中国香港 / 中国台湾专用订阅**，62 条，全部实测通过 |
| `dist/online-new.m3u` | **本次在线新找到的 44 条**，独立订阅，不含任何旧归档地址 |
| `source/online-new.m3u` | 新源的手工维护文件，与 `source/tv.m3u` 旧归档分开 |
| `dist/online-probe.tsv` | 786 条在线候选的逐条判定 |
| `dist/online-sources.tsv` | 本次拉取的 29 个在线源地址与状态 |
| `dist/three-archive.m3u` | 上一轮旧归档的港台澳候选恢复包，278 条，标注 `[未验证]`，不进主订阅 |
| `dist/hk-probe.tsv` | 上一轮 160 条旧香港候选的逐条判定 |
| `dist/sports.m3u` | **NBA / 格斗 / 赛事台体育专用订阅**，49 条，全部实测通过 |
| `source/sports.m3u` | 体育源的手工维护文件，与旧归档分开 |
| `dist/sports-probe.tsv` | 182 条体育候选的逐条判定 |
| `dist/sports-sources.tsv` | 本轮拉取的 8 个体育公开列表地址与状态 |

## 怎么加源

两种方式。

**手工加**：在 `source/` 下的 txt 或 m3u 里加一行 `频道名,地址`，提交，工作流会自动跑一遍。格式见 `source/README.md`。

**让机器自己找**：`config.json` 里的 `remote` 可以填一组每日拉取的公开源地址，清洗时和手工源合在一起验证。目前**留空关闭**——之前挂的三个补充源一次带进 1600 多条，单次扫描量翻倍，出口 IP 被限流后 403 误判率飙升，反而把好源判死。想要补充源就往数组里填地址，同时把 `batch_size` 调小些。

## 每天的活

GitHub Actions 每天北京时间 03:00 跑：

1. 读 `source/` 里所有源（`remote` 当前关闭，见上）
2. **小批量**逐条探测：每批 50 条、批间冷却 5 秒、批内并发 8。先拿 m3u8，再往下追到分片真下到数据才算通过
3. 跑完隔一段时间再抓一次列表，序列号不前进的判为循环回放
4. 403/429 之类软失败冷却后低速复核，仍失败才删
5. 重写 `dist/` 并自动提交

手动触发：Actions 页 → 清理直播源 → Run workflow。

## 本地跑和 Actions 跑，结果不一样

这件事得说清楚，否则会以为订阅被改坏了。

**Actions 的出口 IP 在境外**。国内那些只允许大陆访问的源（咪咕、中移动系、部分省市台）在 runner 上会全部连不上；反过来，境内被墙的源在 runner 上反而能通。同一份源，两边结论能对不上的比例不低。

所以 `config.json` 里分了两套策略：

| 环境 | 策略 |
| --- | --- |
| 本地（国内 IP） | `drop_unverified: true` — 只把实测通过的写进订阅，其余全部移出 |
| GitHub Actions | `drop_unverified_in_ci: false` — 保守模式，只删确认失效的，不删存疑的，**且不覆盖根目录 `tv.m3u`** |

本地那份干净订阅推上去之后，Actions **不会**拿境外 IP 的结论覆盖根目录 `tv.m3u`。但 `dist/` 里的 `all.m3u`、`all_status.m3u` 和六个分类文件会被 CI 按保守模式重写，条数会比本地版多不少——多出来的是「境外连不上、境内未必不能播」的源。**播放器只订阅根目录 `tv.m3u`，别用 `dist/all.m3u`。** 每次本地重跑清洗会把这些文件同步回本地结论。

想要长期自动剔除，最靠谱的是在国内网络（本机、NAS、软路由）给 `scripts/clean.py` 挂个定时任务。真要让 CI 也执行剔除，把 `drop_unverified_in_ci` 改成 `true`，代价是可能误删只允许大陆访问的源。

## 剔除是怎么判的

这套东西最大的坑是限流误判。实测连续扫完 2800 条后有 1979 条被判 403，跑完串行抽查 18 条，其中 9 条返回 200——一半是误杀。短时间内上万次请求把出口 IP 打进了限流状态，冷却 20 秒、40 秒都不够，复核阶段自己也还在被限流。

所以**限速是第一手段**：每批 50 条、批间冷却 5 秒、批内并发 8，而且只核实主源，不把自动搜集的 1600 条混进来凑数。403/429 仍不直接判死，整轮结束后冷却一轮，用**条目自带的 UA 和 Referer** 低速复核。这里不能换成浏览器 UA——带自定义 UA 的样本用自带 UA 有 7/14 能通，换浏览器 UA 只剩 2/14。

**如果整轮跑完 403 还是成片，别采信那一轮的结果。** 等十几分钟让出口 IP 缓过来，再执行补核：

```
python scripts/clean.py --config recheck_config.json --recheck
```

它读上一轮的 `dist/detail.tsv`，不重跑主探测，只把没通过的条目以**单并发**逐条重测，批间留冷却。实测并发越高 403 越多：8 并发只剩 5%，4 并发复核救回 1%，纯串行抽查却有 30%–50% 能通。批量扫描期间被限流误杀的源，靠这一步捞回来。

复核之外还有几档：

| 档位 | 依据 | 处理 |
| --- | --- | --- |
| 通过 | 拿到 m3u8，追到分片真读到数据，且列表还在前进 | 写入订阅 |
| 存疑 | IPv6 源、rtmp 非 http、加密流、分片被反盗链挡住 | 移出订阅，另存 `pending.m3u` |
| 死亡 | 404、连接被拒、超时、TLS 握手失败、返回 HTML、多轮复核仍 403 | 删除，记入 `removed.tsv` |

**播放列表停滞**单独一档。有些源分片能正常下载，但 m3u8 里的媒体序列号长时间不前进，播放器会把那几十秒画面无限循环——看着像在播，其实内容早卡死了。跑完一轮隔 90 秒再抓一次列表，序列号没动就标成循环回放。2026 年 1 月起中国蓝（cztv）那批 lantian 源全挂成这个样子，就是靠这条检测抓出来的。凌晨县市台停播时列表也会冻住，那是正常状态，白天会自己恢复。

## 403 不等于源死了

2026-11-07 终审后又单独复查过：那批 1ms 返回的 403，响应体是空的、没有 Server 头，
有的连 TCP 都没建连成功，HTTP 层却直接给了 403。这是本机网络中间层拦截，不是源站拒绝。
CCTV 全系、CGTN、各卫视 4K 整批消失主要是这个原因，不是频道集体停播。

同一次抽查里，写入订阅的源抽 18 条全部返回 200 且是可用的播放列表，
`removed.tsv` 里抽 20 条则无一可拉流。也就是说：**保留下来的这部分是可靠的，
被删掉的那部分只代表本机连不到**。换个网络或直接用播放器，其中一些大概率还能看。

想找回某条，去 `dist/removed.tsv` 翻完整地址和原始 UA／Referer，
抄回 `source/tv.m3u` 就行。`source/tv.m3u` 原有 1287 条归档一条没删，
末尾追加过 13 条，现 1300 条；在线新源另放 `source/online-new.m3u`（44 条），
体育源另放 `source/sports.m3u`（49 条），三份互不覆盖。
详见 `dist/report.md` 的「交叉验证」和「判定边界」两节。

## 央视、香港、台湾频道（在线新源）

上一轮一直围着 `source/tv.m3u` 那批旧地址复核，香港源怎么试都被本机网络挡住。
这一轮改成**在线重新找**：搜了 29 个仍在自动更新的公开列表，成功拉到 22 个
（bestK/iptv 每小时检测、MercuryZz/IPTVN 港澳台专题、epg.pw 分地区列表、
live.zbds.top、YueChan、Kimentanm、iptv-org 网站版等），只从这批新列表里提取三类频道。
**旧归档一条没读、一条没改**，已经在订阅里的地址也全部排除。

| 步骤 | 数量 |
| --- | --- |
| 成功拉取的在线列表 | 22 / 29 |
| 提取出的全新候选 | 786（央视 303 / 香港 243 / 台湾 240） |
| TCP 可建连进入 HTTP 复核 | 284 |
| 拿到有效播放列表 | 147 |
| 两轮活性判定通过 | 67 |
| 严格归类、每频道 2 条线路 | 48 |
| 剔掉与旧归档撞车的 6 条，加香港补测 2 条 | **44 条新增** |

44 条全新线路：央视 28（CCTV2/5/8/12/15/16、CGTN 多语种、央视数字付费频道、央广）、
中国台湾 13（台视新闻、民视新闻、TVBS 亚洲、东森超视、TTV News、Dali TV）、
中国香港 3（Jade 翡翠台、Asian Drama、美亚电影台）。
每条都过了「追到分片 + 隔 20 秒序列号前进」两关，不是循环回放的僵尸列表。

订阅地址：

```
https://raw.githubusercontent.com/Zoramartina/OKK/main/tv.m3u              主订阅 185 条（全量）
https://raw.githubusercontent.com/Zoramartina/OKK/main/dist/cctv-hk-tw.m3u  央视 / 港 / 台专用 62 条
https://raw.githubusercontent.com/Zoramartina/OKK/main/dist/online-new.m3u  在线新增 44 条
https://raw.githubusercontent.com/Zoramartina/OKK/main/dist/sports.m3u       NBA / 格斗 / 赛事台 49 条
```

新源单独放在 `source/online-new.m3u`，和 `source/tv.m3u` 那 1300 条旧归档分开，
清洗脚本会同时读这两个文件。要删这批源，只动 `online-new.m3u` 就行。

**归类有个坑**：`freetv`、`bigbig` 是国际聚合源，靠短关键词会把
AlphaTV（希腊）、Knesset（以色列）、RadioItaliaTV（意大利）当成港台，
TVBS 也会因为名字含 `tvb` 被误判成香港。终审后加了严格品牌词白名单重新归类，
剔掉 16 条外国台，判定顺序也改成台湾优先。逐条结果见 `dist/online-probe.tsv`，
源地址见 `dist/online-sources.tsv`。

香港仍然受地区限制：243 条候选里 153 条跨境 TCP 未建连，RTHK 全系返回真实地区限制 403。
把「拿到列表但追分片超时」的挑出来用 6 秒超时单独补测，又捞回 2 条。
上一轮那份 `dist/three-archive.m3u` 是旧归档的备选地址，本次没有再碰，
需要时仍可自行导入试；`dist/hk-probe.tsv` 是它的逐条判定。

## 体育频道：看 NBA 和格斗

这一轮同样**只从在线公开列表里找**，旧归档 `source/tv.m3u` 一条没读。
新拉了 5 份列表：iptv-org 网站版 `categories/sports.m3u`（479 条）、
iptv-org 的 us / uk / tw 分区列表、Guovin/iptv-api 的每日结果；
加上上一轮已缓存的 22 份在线列表，共 27 份作为候选来源。
源地址与状态在 `dist/sports-sources.tsv`。

| 阶段 | 条数 |
| --- | --- |
| 严格归类的全新候选 | 182（赛事台 149 / 格斗 27 / 篮球 6） |
| TCP 预筛：86 个 host，可建连 67 | 进入 HTTP 复核 121 |
| 拿到有效播放列表 | 70 |
| 两轮活性指纹通过 | 48 |
| 长超时补测（追 variant）再捞回 | +5 |
| 合并去重、语义清洗剔 1 条误判 | **49 条新增** |

主订阅 136 → **185 条**，体育单独出一份 `dist/sports.m3u`，分三组：

| 分组 | 条数 | 代表频道 |
| --- | --- | --- |
| `体育·NBA` | 1 | NBA TV (720p) |
| `体育·格斗` | 7 | FightBox / FightBox HD / FightBox Poland、DAZN 3 Portugal、MMA-TV.com、Persiana Fight、TVS Boxing |
| `体育·赛事台` | 41 | CCTV-5 / 5+ / 16、五星体育、广东体育、山东体育、天津体育、ESPN 系列、TNT Sports、beIN SPORTS XTRA、Eurosport、Eleven Sports、Arena Sport |

**看比赛要挑台**：NBA TV 是全天篮球台；国内看 NBA 主要靠 CCTV-5 / 5+、五星体育、广东体育，
境外靠 ESPN、TNT Sports。格斗（UFC、拳击、MMA、踢拳）靠 `体育·格斗` 那 7 条，
另外 DAZN、TNT Sports 这类赛事台在有大赛时也会转播。这些都是转播台而非赛事专场，
有没有比赛要看当日节目表，不是点开就有 NBA 或 UFC。

体育源独立放在 `source/sports.m3u`，配置里新增了 `sports.m3u` 分类文件并放在匹配顺序第一位，
这样 CCTV-5 这类名称含「CCTV」的体育台不会被归到央视频道分类去。

顺手修了 `scripts/clean.py` 的一个解析 bug：`#EXTINF` 属性里的 UA 常带逗号
（`(KHTML, like Gecko)`），原来按第一个逗号切分会把它后半截当成频道名，
产出一批 `Chrome/149.0.0.0 Safari/...` 这样的乱码条目；现在改成按**引号外的第一个逗号**切。
归类也换成品牌词白名单 + 英文短词边界，避免 `pinball` 里藏着 `nba`、
`Drammatico` 里藏着 `mma` 这种误判，并剔掉了误入的 His Glory TV（宗教台）。
逐条判定见 `dist/sports-probe.tsv`。

判定边界和前几轮一样：这里的「可用」只代表跑清洗这台机器能拉到流且序列号在前进，
不保证节目内容、也不保证换网络后仍然可播。

## 另外两条

**`http-user-agent` 会参与探测并原样写回**。原文件里 42 条源靠这个属性能播，统一用浏览器 UA 会把它们全判死。

**主源的线路不会被砍**。同一个频道留多少条线路由你手工决定，脚本不清洗这块。自动搜集来的源才会限制每频道最多 3 条（`config.json` 里的 `max_per_channel`）。

## 版权

只处理地址，不碰内容。源都是第三方转播，自用即可。
