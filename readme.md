基于搜狗微信搜索的微信公众号爬虫接口
===


# 项目简介
基于搜狗微信搜索的微信公众号爬虫接口，可以扩展成基于搜狗搜索的爬虫

基于Python3

如果有问题，请提issue

> 关于我，欢迎关注
  微博：[Chyroc](http://weibo.com/cyp1105)
---

# 项目使用

参见[test.py](https://github.com/Chyroc/WechatSogou/blob/master/test.py)

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

## 获取最近文章 详情页 字典 - get_gzh_recent_info

    wechat_id = 'nanhangqinggong'
    wechat_info = wechats.get_gzh_info(wechat_id)
    data = wechats.get_gzh_recent_info(wechat_info['url'])

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_article_and_gzh_by_url_dict.png" />


字段|含义
---|---
gzh_info|公众号信息字典
articles|最近文章列表，每一项均是字典

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

`articles`的每一项具体如下

字段|含义
---|---
main|是否是一次推送中第一篇文章，1则是
title|文章标题
digest|摘要
content|
fileid|
content_url|文章地址
source_url|原文地址
cover|封面图片
author|作者
copyright_stat|文章内容版权性


## 通过微信号获取上一步数据 - get_gzh_article_by_wechatid_dict

    wechat_id = 'nanhangqinggong'
    articles_by_wechatid = wechats.get_gzh_article_by_wechatid_dict(wechat_id)

返回结果与上一步一样


## 处理文章 - get_gzh_article_info

一般需要处理，因为需要在这一步获取固定的而不是临时的文章链接

    wechat_id = 'nanhangqinggong'
    wechat_info = wechats.get_gzh_info(wechat_id)
    articles = wechats.get_gzh_article_by_url_dict(wechat_info['url'])
    article_info = wechats.get_gzh_article_info(articles[0])

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_article_info.png" />

返回字典，具体如下

字段|含义
---|---
yuan|文章固定地址
related|相似文章信息字典
comment|评论信息字典
content|文章内容


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
其余字典未说明，请打印自行查看|

`content`是文章内容，字典，一下三项均含`img`和`br`标签

字段|含义
---|---
content_html|原始文章内容，包括html标签及样式
content_rich|包含图片（包括图片应展示的样式）的文章内容
content_text|包含图片（`<img src="..." />`格式）的文章内容

## 获取首页推荐文章公众号最近文章地址 - get_recent_article_url_by_index_single

    articles_single = wechats.get_recent_article_url_by_index_single()

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_recent_article_url_by_index_single.png" />

返回的是列表，每一项是不同公众号的的最近文章页

## 获取首页推荐文章公众号最近文章地址  所有分类 - get_recent_article_url_by_index_all

    articles_all = wechats.get_recent_article_url_by_index_all()

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_recent_article_url_by_index_all.png" />


返回的是列表，每一项是不同公众号的的最近文章页

---

# TODO
- [x] 相似文章的公众号获取
- [x] 主页热门公众号获取
- [x] 文章详情页信息
- [ ] 验证码识别
- [ ] 接入爬虫框架
- [ ] 兼容py2

---