基于搜狗微信搜索的微信公众号爬虫接口
===


# 项目简介
基于搜狗微信搜索的微信公众号爬虫接口，可以扩展成基于搜狗搜索的爬虫
基于Python3，但是2应该也可以使用
> 关于我，欢迎关注
  微博：[Chyroc](http://weibo.com/cyp1105)
  邮箱：chyroc@qq.com
---

# 项目使用

## 引用

    from wechatsogou import wechatspider
    wechats = wechatspider()
    wechats.get_session()

## 搜索公众号 - search_gzh_info

    infos = wechats.search_gzh_info(name, page)
    for info in infos:
        name = info['name']
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
对于一个已知`wechatid`的公众号，如果需要获取其最近文章，可以通过以下方式先获取具体信息（包括最近文章地址），然后根据``获取

    detail = wechats.get_gzh_info(wechatid）
    url = detail['url']
返回结果与上述search_gzh_info函数返回结果一致

## 获取最近文章列表字典 - get_gzh_article_dict

    msgdict = wechats.get_gzh_article_dict(url)
msgdict是字典

字段|含义
---|---
list|只有这一个字段，包含具体信息


    infos = msgdict['list']
    for info in infos:
        comm_msg_info = info['comm_msg_info']
        app_msg_ext_info = info['app_msg_ext_info']

comm_msg_info是字典

字段|含义
---|---
status|...
fakeid|...
datetime|...
type|...
id|...
content|...

app_msg_ext_info也是字典

字段|含义
---|---
subtype|...
title|标题
copyright_stat|文章类型（100为普通，11原创，101转载）
author|作者
source_url|原文地址
fileid|...
content|...
content_url|文章地址
cover|封面图片地址
digest|描述
is_multi|是否多图文（1位多图文，有multi_app_msg_item_list字段，0为单图文）
multi_app_msg_item_list|多图文

## 获取最近文章列表 - get_gzh_article_detail

    msgdict = wechats.get_gzh_article_dict(url)
    item = wechats.get_gzh_article_detail(msgdict)
item是列表，每一项均是具体信息字典

字段|含义
---|---
title|标题
digest|描述
cover|封面图片地址
main|是否为一次推送中第一篇文章
content_url|文章地址
author|作者
copyright_stat|文章类型（100为普通，11原创，101转载）
source_url|原文地址
fileid|...
content|...

## 获取文章具体信息 - get_get_gzh_article_info

    infos = wechats.get_gzh_info('newsbro')
    articledict = wechats.get_gzh_article_dict(infos['url'])
    articles = wechats.get_gzh_article_detail(articledict)
    for article in articles:
        article_info = wechats.get_get_gzh_article_info(article)

article_info是文章页具体信息字典

字段|含义
---|---
yuan|文章的固定地址（通过搜索获取的文章地址有时效性？）
content|文章内容，字典，一下三项均含img和br标签
content->content_html|原始文章内容，包括html标签及样式
content->content_rich|包含图片（包括图片应展示的样式）的文章内容
content->content_text|包含图片（<img src="..." />格式）的文章内容
comment|评论以及阅读量，字典
comment->base_resp|返回码，字典，包含下面两项
comment->base_resp->ret|返回码
comment->base_resp->errmsg|返回错误信息
comment->read_num|阅读量
comment->like_num|点赞数
comment->elected_comment_total_cnt|评论数
comment->comment|具体评论数据，每一项均是一个列表，设为comment_comment

comment_comment是一项评论

字段|含义
---|---
content|评论内容
like_num|点赞数
nick_name|评论者昵称
logo_url|评论者头像
reply|回复
其余字典未说明，请打印自行查看|

---

# TODO
- [ ] 相似文章的公众号获取
- [ ] 主页热门公众号获取
- [x] 文章详情页信息

---