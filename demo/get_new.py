# -*- coding: utf-8 -*-
from wechatsogou import *
from wechatsogou.exceptions import *
from wechatsogou.tools import *

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


class UpdateArticls(object):
    def __init__(self, wechatid, table, pre, ocr_config=None):
        if ocr_config:
            self.wechats = WechatSogouApi(ocr_config=ocr_config)
        else:
            self.wechats = WechatSogouApi()
        self.wechatid = wechatid
        self.cache = WechatCache()
        self.m = mysql(table, pre)

    def save(self, messages):
        for message in messages:
            if int(message['type']) == 49:
                try:
                    yuan = self.wechats.deal_article_yuan(url=message['content_url'])
                except WechatSogouBreakException:
                    continue

                url_param = get_url_param(yuan)
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
                message_save['article_url'] = yuan
                message_save['content_url'] = message['content_url']
                message_save['source_url'] = message['source_url']
                message_save['post_date'] = message['datetime']
                message_save['msgid'] = msgid  # 去重

                self.m.add(message_save)

                print('deal article ' + yuan)

    def cache_rencent_url(self, url=None):
        if url:
            self.cache.set(self.wechatid + 'recent_url', url, 0)
        else:
            return self.cache.get(self.wechatid + 'recent_url')

    def run(self):
        url = self.cache_rencent_url()

        if not url:
            print('get recent url from wechatid')
            gzh_info = self.wechats.get_gzh_info(self.wechatid)
            url = gzh_info['url']
            self.cache_rencent_url(url)
        else:
            print('get recent url from cache')

        gzh_messages = self.wechats.get_gzh_message(url=url)

        print(gzh_messages)

        self.save(gzh_messages)

        print('end.')


if __name__ == '__main__':
    wechatid = '........'
    ocr_config = {
        'type': 'ruokuai',
        'dama_name': '',
        'dama_pswd': '',
        'dama_soft_id': '',
        'dama_soft_key': ''
    }
    UpdateArticls(w['id'], 'article', 'yu', ocr_config).run()
