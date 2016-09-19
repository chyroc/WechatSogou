# -*- coding: utf-8 -*-
from wechatsogou import *
from wechatsogou.exceptions import *

"""
创建表

CREATE TABLE IF NOT EXISTS `pre_article` (
  `aid` int(10) NOT NULL AUTO_INCREMENT,
  `mp_id` varchar(50) NOT NULL,
  `title` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `post_user` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL,
  `post_date` int(15) NOT NULL,
  `brief_content` varchar(300) CHARACTER SET utf8mb4 DEFAULT NULL,
  `fileid` int(20) NOT NULL,
  `thumb` text CHARACTER SET utf8mb4,
  `content_url` text CHARACTER SET utf8mb4,
  `article_url` text NOT NULL,
  `source_url` text CHARACTER SET utf8mb4,
  `qunfa_id` int(20) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `fileid` (`fileid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
"""


class DownArticles(object):
    """获取存储所有群发消息
    """

    def __init__(self, wechatid, url, table, pre):
        self.wechats = WechatSogouApi()
        self.wechatid = wechatid
        self.url = url
        self.m = mysql(table, pre)

    def save(self, messages):
        for message in messages:
            if int(message['type']) == 49:
                message_save = dict()
                message_save['mp_id'] = wechatid
                message_save['post_user'] = message['author']
                message_save['title'] = message['title']
                message_save['thumb'] = message['cover']
                message_save['brief_content'] = message['digest']
                message_save['article_url'] = message['content_url']
                message_save['content_url'] = message['content_url']
                message_save['source_url'] = message['source_url']
                message_save['post_date'] = message['datetime']
                message_save['fileid'] = message['fileid']  # 去重
                message_save['qunfa_id'] = message['qunfa_id']

                self.m.add(message_save)

    def save_first(self):
        print('msgid ', self.wechats._uinkeybiz(self.wechatid)[4])
        messages = self.wechats.deal_mass_send_msg(url, wechatid)
        self.save(messages)

    def save_next(self, updatecache=True):
        print('msgid ', self.wechats._uinkeybiz(self.wechatid)[4])
        try:
            messages = self.wechats.deal_mass_send_msg_page(wechatid, updatecache)
            self.save(messages)
        except WechatSogouEndException:
            print('end.')
            exit()

    def run(self):
        try:
            self.save_next(False)
            print('next is ok')
            while True:
                self.save_next()
        except (WechatSogouHistoryMsgException, TypeError):
            try:
                print('from url start')
                self.save_first()
                while True:
                    self.save_next()
            except WechatSogouHistoryMsgException:
                print('next is error. need new url')


if __name__ == '__main__':
    wechatid = 'xxxxxxxxxxxx'
    url = 'http://mp.weixin.qq.com/mp/getmasssendmsg?..................'

    DownArticles(wechatid, url, 'article', 'pre').run()
