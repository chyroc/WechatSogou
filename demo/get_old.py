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


class DownArticles(object):
    """获取存储所有群发消息
    """

    def __init__(self, wechatid, url, **kwargs):

        ocr_config = kwargs.get('ocr_config')
        if ocr_config:
            self.wechats = WechatSogouApi(ocr_config=ocr_config)
        else:
            self.wechats = WechatSogouApi()

        self.save_func = kwargs.get('save_func')

        self.wechatid = wechatid
        self.url = url

    def save(self, messages):
        if callable(self.save_func):
            articles = self.dealkey(messages)
            self.save_func(articles)
            print('saved')
        else:
            print('no save_func, do nothing')

    def dealkey(self, messages):
        articles = []

        for message in messages:
            if int(message['type']) == 49:
                url_param = get_url_param(message['content_url'])
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
                article['url'] = message['content_url']
                article['source_url'] = message['source_url']
                article['pushTime'] = message['datetime']

                article['source_url'] = message['source_url']  # 左下角原文地址
                article['msgid'] = msgid  # 去重

                articles.append(article)

        return articles

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
    ocr_config = {
        'type': 'ruokuai',
        'dama_name': '',
        'dama_pswd': '',
        'dama_soft_id': '',
        'dama_soft_key': ''
    }


    def save_func(articles):
        """自定义的数据处理保存函数

        ::param articles 文章字段字典的列表
        """
        print(articles)


    DownArticles(wechatid, url, ocr_config=ocr_config, save_func=save_func).run()
