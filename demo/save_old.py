# -*- coding: utf-8 -*-
from wechatsogou import *
from demo.get_old import DownArticles
from demo.save_by_leancloud import SaveLcoud
from datetime import datetime


def save_old_article(wechatid, url, table='Article_MP'):
    def save_func(articles):
        for article in articles:
            article['pushTime'] = datetime.fromtimestamp(article['pushTime'])

        sl.save(table, articles)

    DownArticles(wechatid, url, ocr_config=ocr_config, save_func=save_func).run()


if __name__ == '__main__':
    ocr_config = {
        'type': 'ruokuai',
        'dama_name': '',
        'dama_pswd': '',
        'dama_soft_id': '',
        'dama_soft_key': ''
    }

    appid = ''
    appkey = ''
    sl = SaveLcoud(appid=appid, appkey=appkey)

    wechatid = '..........'
    url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?...............'

    save_old_article(wechatid, url, 'Article_MP')  # 保存wechatid的历史文章
