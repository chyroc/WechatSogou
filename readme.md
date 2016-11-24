基于搜狗微信搜索的微信公众号爬虫接口
===


![py27](https://camo.githubusercontent.com/392a32588691a8418368a51ff33a12d41f11f0a9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d322e372d6666363962342e737667) ![py35](https://camo.githubusercontent.com/633acad03f4dbbaa8cca6bee5902207fd3b27a34/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e352d7265642e737667)

# 赞助作者
学生党，过年想攒个PS4，各位好汉乐意就给个赞助~

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/pay_zfb.jpg" width="250" />
<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/pay_wx.jpg" width="250" />

# 项目简介
基于搜狗微信搜索的微信公众号爬虫接口，可以扩展成基于搜狗搜索的爬虫

如果有问题，请提issue


# 项目使用

参见[test.py](https://github.com/Chyroc/WechatSogou/blob/master/test.py)

## 日志

    import logging
    import logging.config
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
## 引用

    from wechatsogou import *
    wechats = WechatSogouApi()

## 搜索公众号 - search_gzh_info

    name = '南京航空航天大学'
    wechat_infos = wechats.search_gzh_info(name)

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/search_gzh_info.png" />

返回结果是列表，每一项均是公众号具体信息字典，具体如下

字段|含义
---|---
name|公众号名称
wechatid|公众号ID
jieshao|介绍
renzhen|认证信息，为空表示未认证
qrcode|二维码图片地址
img|头像地址
url|最近文章地址

## 获取公众号
对于一个已知`wechatid`的公众号

    wechat_id = 'nanhangqinggong'
    wechat_info = wechats.get_gzh_info(wechat_id)

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_info.png" />

返回结果与上述search_gzh_info返回结果一致


## 搜索微信文章

    keywords = '傅里叶变换'
    wechat_articles = wechats.search_article_info(keywords)

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/search_article_info.png" />

返回结果是列表，每一项均是文章信息字典，具体如下

字段|含义
---|---
name|文章标题
url|文章链接
img|文章封面图片缩略图，可转为高清大图
zhaiyao|文章摘要
time|文章推送时间，10位时间戳
gzhname|公众号名称
gzhqrcodes|公众号二维码
gzhurl|公众号最近文章地址


## 解析最近文章页  或  解析历史消息记录 - get_gzh_message

    data = wechats.get_gzh_message(url=url)
    # 或者 data = wechats.get_gzh_message(wechatid=wechatid)
    # 或者（不推荐） data = wechats.get_gzh_message(wechat_name=wechat_name)

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_message.png" />

返回的是 列表，每一项均是字典，一定含有字段qunfa_id,datetime,type

字段|含义
---|---
qunfa_id|群发消息id
datetime|群发10位时间戳
type|群发消息类型

下面是type不同的值时的其他字段

字段|含义
---|---
type|1,表示文字
content|文字内容

字段|含义
---|---
type|3,表示图片
img_url|图片链接

字段|含义
---|---
type|34,表示音频
play_length|长度
fileid|id
audio_src|音频地址

字段|含义
---|---
type|49,表示图文
main|是否是一次推送中第一篇文章，1则是
is_multi|本图文所属推送是否是多图文
title|文章标题
digest|摘要
fileid|id
content_url|文章地址
source_url|原文地址
cover|封面图片
author|作者
copyright_stat|文章内容版权性

字段|含义
---|---
type|62,表示视频
cdn_videoid|id
thumb|缩略图
video_src|视频地址

## 解析公众号信息  和  最近群发文章 - get_gzh_message_and_info

    data = wechats.get_gzh_message_and_info(url=url)
    # 或者 data = wechats.get_gzh_message_and_info(wechatid=wechatid)
    # 或者（不推荐） data = wechats.get_gzh_message_and_info(wechat_name=wechat_name)

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_message_and_info.png" />

返回的是字典{'gzh_info':gzh_info, 'gzh_messages':gzh_messages}

字段|含义
---|---
gzh_info|公众号信息字典
gzh_messages|群发消息列表

其中`gzh_info`的具体如下

字段|含义
---|---
name|公众号名称
wechatid|公众号id
jieshao|介绍
renzhen|认证，为空表示未认证
qrcode|二维码
img|头像图片
url|最近文章地址

`gzh_messages`一定含有字段qunfa_id,datetime,type
具体见上一项

## 获取文章内容 - deal_article_content

    article_content = wechats.deal_article_content(text=text)
    # 或 article_content = wechats.deal_article_content(url=url)

`text`是文章页文本，`url`是文章页链接

返回是文章内容（含有html格式）

## 获取相似文章 - deal_article_related

    article_related = wechats.deal_article_related(url, title)

`url`: 文章链接,`title`: 文章标题

## 获取文章评论 - deal_article_comment

    article_comment = wechats.deal_article_comment(text=text)
    # 或 article_comment = wechats.deal_article_comment(url=url)

`text`是文章页文本，`url`是文章页链接

## 获取文章以上三项信息 - deal_article

一般需要处理，因为需要在这一步获取固定的而不是临时的文章链接

    article_info = wechats.deal_article(url)

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/deal_article.png" />

返回字典，具体如下

字段|含义
---|---
yuan|文章固定地址
related|相似文章信息字典
comment|评论信息字典
content_html|文章内容


`comment`是评论以及阅读量，字典

字段|含义
---|---
base_resp|返回码，字典，包含下面两项
base_resp->ret|返回码
base_resp->errmsg|返回错误信息
read_num|阅读量
like_num|点赞数
elected_comment_total_cnt|评论数
comment|具体评论数据，每一项均是一个列表，设为comment_comment

`comment_comment`是一项评论

字段|含义
---|---
content|评论内容
like_num|点赞数
nick_name|评论者昵称
logo_url|评论者头像
reply|回复
其余字典未说明，请打印自行查看|...

## 获取首页推荐文章公众号最近文章地址 - get_recent_article_url_by_index_single

    articles_single = wechats.get_recent_article_url_by_index_single()

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_recent_article_url_by_index_single.png" />

返回的是列表，每一项是不同公众号的的最近文章页

## 获取首页推荐文章公众号最近文章地址  所有分类 - get_recent_article_url_by_index_all

    articles_all = wechats.get_recent_article_url_by_index_all()

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_recent_article_url_by_index_all.png" />


返回的是列表，每一项是不同公众号的的最近文章页

## 获取微信搜狗搜索关键词联想 - get_sugg

    sugg_keyword = wechats.get_sugg('中国梦')

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_sugg.png" />


返回的是列表，每一项是不同公众号的的最近文章页

---

# TODO
- [x] 相似文章的公众号获取
- [x] 主页热门公众号获取
- [x] 文章详情页信息
- [x] 所有类型的解析
- [ ] 验证码识别
- [ ] 接入爬虫框架
- [ ] 兼容py2

---