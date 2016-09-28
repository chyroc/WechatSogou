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


class UpdateArticls(object):
    def __init__(self, wechatid, **kwargs):

        ocr_config = kwargs.get('ocr_config')
        if ocr_config:
            self.wechats = WechatSogouApi(ocr_config=ocr_config)
        else:
            self.wechats = WechatSogouApi()

        self.save_func = kwargs.get('save_func')

        self.wechatid = wechatid
        self.cache = WechatCache()

    def save(self, gzh_messages):
        if callable(self.save_func):
            articles = self.dealkey(gzh_messages)
            self.save_func(articles)
            print('saved')
        else:
            print('no save_func, do nothing')

    def dealkey(self, messages):
        articles = []

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

                article = dict()
                article['wechatID'] = self.wechatid
                article['authorName'] = message['author']
                article['title'] = message['title']
                article['thumbnails'] = message['cover']
                article['summary'] = message['digest']
                article['url'] = yuan
                article['pushTime'] = message['datetime']

                article['source_url'] = message['source_url']  # 左下角原文地址
                article['msgid'] = msgid  # 去重

                articles.append(article)

        return articles

    def cache_rencent_url(self, url=None):
        if url:
            self.cache.set(self.wechatid + 'recent_url', url, 5 * 3600)
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


    def save_func(articles):
        print(articles)


    UpdateArticls(wechatid, ocr_config=ocr_config, save_func=save_func).run()
