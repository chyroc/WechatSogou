# -*- coding: utf-8 -*-
from wechatsogou import *
from wechatsogou.exceptions import *

try:
    import urlparse as url_parse
except ImportError:
    import urllib.parse as url_parse


def get_url_param(url):
    result = url_parse.urlparse(url)
    url_param = url_parse.parse_qs(result.query, True)
    biz = url_param.get('__biz')[0] if url_param.get('__biz') else ''
    sn = url_param.get('sn')[0] if url_param.get('sn') else ''
    mid = url_param.get('mid')[0] if url_param.get('mid') else ''
    return {'biz': biz, 'sn': sn, 'mid': mid}


"""
创建表

CREATE TABLE IF NOT EXISTS `yu_article` (
  `aid` int(10) NOT NULL AUTO_INCREMENT,
  `mp_id` varchar(50) NOT NULL,
  `title` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `post_user` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL,
  `post_date` int(15) NOT NULL,
  `brief_content` varchar(300) CHARACTER SET utf8mb4 DEFAULT NULL,
  `thumb` text CHARACTER SET utf8mb4,
  `content_url` text CHARACTER SET utf8mb4,
  `article_url` text NOT NULL,
  `source_url` text CHARACTER SET utf8mb4,
  `msgid` varchar(100) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `msgid` (`msgid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2049 ;
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

                url_param = get_url_param(message['content_url'])
                msgid = ''
                msgid = msgid + 'biz=' + url_param['biz'] + '&'
                msgid = msgid + 'sn=' + url_param['sn'] + '&'
                msgid = msgid + 'mid=' + url_param['mid']

                message_save = dict()
                message_save['mp_id'] = self.wechatid
                message_save['post_user'] = message['author']
                message_save['title'] = message['title']
                message_save['thumb'] = message['cover']
                message_save['brief_content'] = message['digest']
                message_save['article_url'] = message['content_url']
                message_save['content_url'] = message['content_url']
                message_save['source_url'] = message['source_url']
                message_save['post_date'] = message['datetime']
                message_save['msgid'] = msgid  # 去重

                try:
                    self.m.add(message_save)
                except Exception as e:
                    print(e)
                    print(message_save)
                    exit()

    def save_first(self):
        print('msgid ', self.wechats._uinkeybiz(self.wechatid)[4])
        self.wechats.deal_mass_send_msg(self.url, self.wechatid)

    def save_next(self, updatecache=True):
        print('msgid ', self.wechats._uinkeybiz(self.wechatid)[4])
        try:
            messages = self.wechats.deal_mass_send_msg_page(self.wechatid, updatecache)
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
            except WechatSogouHistoryMsgException as e:
                print('next is error. need new url')
                print(e)


if __name__ == '__main__':
    wechatid = '..........'
    url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?...............'

    DownArticles(wechatid, url, 'article', 'yu').run()
