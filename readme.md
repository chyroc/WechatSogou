基于搜狗微信搜索的微信公众号爬虫接口
===

# 使用
    import wechatsogou as wechats

# 搜索公众号 - search_gzh_info
## 使用

    infos = search_gzh_info(name, page)
    for info in infos:
        name = info['name']
## 返回
返回结果是列表，每一项均是公众号具体信息字典，具体如下
字段|含义
-|-
name|公众号名称
wechatid|公众号ID
jieshao|介绍
renzhen|认证信息，为空表示未认证
qrcode|二维码图片地址
img|头像地址
url|最近文章地址

# 获取公众号
## 使用
对于一个已知`wechatid`的公众号，如果需要获取其最近文章，可以通过以下方式先获取具体信息（包括最近文章地址），然后根据``获取

    detail = get_gzh_info(wechatid）
    url = detail['url']
## 返回
返回结果与上述search_gzh_info函数返回结果一致

# 获取最近文章列表字典 - get_gzh_article_dict

    msgdict = get_gzh_article_dict(url)
msgdict是字典
字段|含义
-|-
list|只有这一个字段，包含具体信息


    infos = msgdict['list']
    for info in infos:
        comm_msg_info = info['comm_msg_info']
        app_msg_ext_info = info['app_msg_ext_info']

comm_msg_info是字典
字段|含义
-|-
status|...
fakeid|...
datetime|...
type|...
id|...
content|...

app_msg_ext_info也是字典
字段|含义
-|-
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

# 获取最近文章列表 - get_gzh_article_detail

    msgdict = get_gzh_article_dict(url)
    item = get_gzh_article_detail(msgdict)
item是列表，每一项均是具体信息字典
字段|含义
-|-
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
