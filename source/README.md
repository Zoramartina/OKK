# source/ 手工维护区

这里放你自己挑的源。根目录的 `tv.m3u` 是从这里生成的，改那边没用，下次跑会被覆盖。

## 格式

m3u 和 txt 都认，子目录也会递归扫描，重复地址自动去掉。

**m3u**（就是你原来的写法，原样搬进来即可）

```m3u
#EXTM3U x-tvg-url="http://epg.51zmt.top:8000/e.xml"
#EXTINF:-1 tvg-name="东方卫视" tvg-logo="https://.../东方卫视4K.png" http-user-agent="aliplayer" group-title="4K频道",东方卫视4K
http://bp-resource-dfl.bestv.cn/148/3/video.m3u8
```

**txt**

```
央视频道,#genre#
CCTV1,http://example.com/cctv1.m3u8
CCTV1,http://example.com/cctv1-b.m3u8
```

## 会被保留的属性

`tvg-id`、`tvg-name`、`tvg-logo`、`group-title`、`http-user-agent`、`http-referer`、`http-header`、`catchup`、`catchup-source`、`playseek`，以及任何其他 `key="value"`，清洗后原样写回。

`http-user-agent` 和 `http-referer` 不只是带过去，探测时也真的会用它们去请求。这点很关键——你这份源里 42 条靠特定 UA 才能播，不按各自的 UA 去测就会误判成失效。

## 注释掉的行

以 `#` 开头的地址行（比如 `#http://101.35.240.114:88/live.php?id=北京卫视`）视为停用，不会参与清洗，也不会出现在输出里。想恢复就去掉行首的 `#`。

## 怎么加新源

直接在文件末尾追加，提交，工作流会自动跑一遍验证。加错了也没关系，验证不过的会被剔掉，原始文件不动。
