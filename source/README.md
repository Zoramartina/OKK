# source/ 手工维护区

只有 `curated.m3u` 一个文件参与清洗，根目录 `tv.m3u` 和 `dist/` 都是从它生成的。改 `tv.m3u` 没用，下次跑会被覆盖。

旧的 1300 条归档已经移到 `../archive/`，不参与清洗，只在需要找回某个源时查。

## 格式

标准 M3U。每条 `#EXTINF` 后跟一行地址，需要 UA 或 Referer 时写成属性：

```m3u
#EXTINF:-1 tvg-name="CCTV-1" group-title="央视频道",CCTV-1
http://example.com/cctv1.m3u8

#EXTINF:-1 tvg-name="某频道" group-title="地方·浙江" http-user-agent="Mozilla/5.0" http-referer="https://example.com/",某频道
http://example.com/live.m3u8
```

## 分组命名

分组名决定它进哪个分类文件，不要随便改：

| group-title | 进哪个文件 |
| --- | --- |
| `央视频道` | `dist/cctv.m3u` |
| `卫视频道` | `dist/weishi.m3u` |
| `地方·浙江`（按省） | `dist/difang.m3u` |
| `体育·赛事台` | `dist/sports.m3u` |
| `电影频道` | `dist/movie.m3u` |
| `凤凰卫视` | `dist/gangao.m3u` |

省级卫视统一放 `卫视频道`，省内地市、县级台放 `地方·省份`。`clean.py` 先按分组整体归类，分组认不出来才按频道名匹配，所以分组写对比名字写对更重要。

## 加源前先自己测

清洗脚本会重测，但放进来的死源会拖慢整轮探测，也会让报告变脏。加之前至少确认：

1. 能拉到 `#EXTM3U`，不是网页或 403、404
2. 列表里有分片，而且是直播列表（没有 `#EXT-X-ENDLIST`）
3. 隔十几秒再抓一次，序列号在前进

只要一条源在多个网络下都不稳，宁可不放。
