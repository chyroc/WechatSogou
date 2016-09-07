# -*- coding: utf-8 -*-

# 导入包
from wechatsogou.tools import *
from wechatsogou import *

# 实例
wechats = WechatSogouApi()

# 搜索一个微信公众号
name = '南京航空航天大学'
wechat_infos = wechats.search_gzh_info(name)

# 对于数据库中的某一个微信号进行搜索
wechat_id = 'nanhangqinggong'
wechat_info = wechats.get_gzh_info(wechat_id)

# 或许可以对用户开放搜索文章的功能~
keywords = '傅里叶变换'
wechat_articles = wechats.search_article_info(keywords)

# 在上面，我们得到过微信号的最近文章页的地址，现在，就去获取该页的数据
articles = wechats.get_gzh_article_by_url_dict(wechat_info['url'])
gzhinfo = wechats.get_gzh_article_gzh_by_url_dict(wechat_info['url'])
# 一般合起来，如下
data = wechats.get_gzh_article_and_gzh_by_url_dict(wechat_info['url'])


# 上面，是先获取最近文章页地址再获取文章列表的，如果希望一步完成，或者最近文章页失效，则
articles_by_wechatid = wechats.get_gzh_article_by_wechatid_dict(wechat_id)

# 对于上面获取的文章链接，需要处理,注意此方法获取的`yuan`字段是文章固定地址，应该存储这个
article_info = wechats.get_gzh_article_info(articles[0])

# 直接获取热门文章
articles_single = wechats.get_recent_article_url_by_index_single()
articles_all = wechats.get_recent_article_url_by_index_all()


prdict(data)