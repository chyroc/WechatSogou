# -*- coding: utf-8 -*-

# 导入包
from wechatsogou.tools import *
from wechatsogou import *
import logging
import logging.config

# 日志
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

# 实例
wechats = WechatSogouApi()
exit()
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
data = wechats.get_gzh_message(wechatid='nanhangqinggong')
data_all = wechats.get_gzh_message_and_info(wechatid='nanhangqinggong')

# 对于上面获取的文章链接，需要处理,注意此方法获取的`yuan`字段是文章固定地址，应该存储这个
messages = wechats.get_gzh_message(wechatid='nanhangqinggong')
for m in messages:
    if m['type'] == '49':
        article_info = wechats.deal_article(m['content_url'])
        # 或 article_info = wechats.deal_article(m['content_url'], m['title'])

# 直接获取热门文章
articles_single = wechats.get_recent_article_url_by_index_single()
articles_all = wechats.get_recent_article_url_by_index_all()

# 微信搜索联想词
sugg_keyword = wechats.get_sugg('中国梦')
