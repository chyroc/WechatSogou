# -*- coding: utf-8 -*-
from wechatsogou import *
from wechatsogou.exceptions import *
from wechatsogou.tools import *
from demo.get_new import UpdateArticls
from demo.save_by_leancloud import SaveLcoud
from datetime import datetime


def save_article(wechatid, table='Article_MP'):
    def save_func(articles):
        for article in articles:
            article['pushTime'] = datetime.fromtimestamp(article['pushTime'])

        sl.save(table, articles)

    UpdateArticls(wechatid, ocr_config=ocr_config, save_func=save_func).run()


def save_author(wechat_list, table='Author_MP'):
    author_list = []
    for w in wechat_list:
        wechatid = w['id']
        author = WechatSogouApi(ocr_config=ocr_config).get_gzh_info(wechatid)
        author_info = {}
        author_info['name'] = author['name']
        author_info['wechatID'] = author['wechatid']
        author_info['details'] = author['jieshao']
        author_info['qrcode'] = author['qrcode']
        author_info['avatar'] = author['img']
        author_info['authenticateName'] = author['renzhen']

        author_list.append(author_info)
        print(author_info)

    sl.save(table, author_list)


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

    wechat_list = [
        {"title": "央视新闻", "id": "cctvnewscenter"},
        {"title": "南方人物周刊", "id": "Peopleweekly"},
    ]

    save_author(wechat_list, 'Author_MP')  # 保存微信号信息

    for w in wechat_list:
        save_article(w['id'], 'Article_MP')  # 保存wechatid的最近文章
