# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import re
import json

from lxml import etree

from wechatsogou.tools import get_elem_text, list_or_empty, replace_html

find_article_json_re = re.compile('var msgList = (.*?)}}]};')


class WechatSogouStructuring(object):
    @staticmethod
    def get_gzh_by_search(text):
        page = etree.HTML(text)
        lis = page.xpath('//ul[@class="news-list2"]/li')
        relist = []
        for li in lis:
            url = li.xpath('div/div[1]/a/@href')
            img = li.xpath('div/div[1]/a/img/@src')
            name = get_elem_text(li.xpath('div/div[2]/p[1]')[0])
            info = get_elem_text(li.xpath('div/div[2]/p[2]')[0])
            post_perm = 0  # TODO 月发文 <script>var account_anti_url = "/websearch/weixin/pc/anti_account.jsp?.......";</script>
            qrcode = li.xpath('div/div[3]/span/img[1]/@src')
            introduction = get_elem_text(li.xpath('dl[1]/dd')[0])
            authentication = li.xpath('dl[2]/dd/text()')
            relist.append({
                'url': url[0],
                'img': img[0],
                'name': name.replace('red_beg', '').replace('red_end', ''),
                'wechat_id': info.replace('微信号：', ''),
                'post_perm': post_perm,
                'qrcode': qrcode[0] if qrcode else '',
                'introduction': introduction.replace('red_beg', '').replace('red_end', ''),
                'authentication': authentication[0] if authentication else ''
            })
        return relist

    @staticmethod
    def get_article_by_search(text):
        page = etree.HTML(text)
        lis = page.xpath('//ul[@class="news-list"]/li')

        articles = []
        for li in lis:
            url = li.xpath('div[1]/a/@href')
            if url:
                title = li.xpath('div[2]/h3/a')
                imgs = li.xpath('div[1]/a/img/@src')
                abstract = li.xpath('div[2]/p')
                time = li.xpath('div[2]/div/span/script/text()')
                gzh_info = li.xpath('div[2]/div/a')[0]
            else:
                url = li.xpath('div/h3/a/@href')
                title = li.xpath('div/h3/a')
                imgs = []
                spans = li.xpath('div/div[1]/a')
                for span in spans:
                    img = span.xpath('span/img/@src')
                    if img:
                        imgs.append(img)
                abstract = li.xpath('div/p')
                time = li.xpath('div/div[2]/span/script/text()')
                gzh_info = li.xpath('div/div[2]/a')[0]

            if title:
                title = get_elem_text(title[0]).replace("red_beg", "").replace("red_end", "")
            else:
                title = ''
            if abstract:
                abstract = get_elem_text(abstract[0]).replace("red_beg", "").replace("red_end", "")
            else:
                abstract = ''

            time = list_or_empty(time)
            time = re.findall('timeConvert\(\'(.*?)\'\)', time)
            time = list_or_empty(time, int)
            gzh_article_url = gzh_info.xpath('@href')
            gzh_headimage = gzh_info.xpath('@data-headimage')
            # gzh_qrcodeurl = gzh_info.xpath('@data-encqrcodeurl')
            gzh_name = gzh_info.xpath('text()')  # gzh_info.xpath('@data-sourcename')
            # gzh_wechatid = gzh_info.xpath('@data-username')
            gzh_isv = gzh_info.xpath('@data-isv')
            # gzh_avgpublish = gzh_info.xpath('@data-avgpublish')
            # gzh_avgread = gzh_info.xpath('@data-avgread')

            articles.append({
                'article': {
                    'title': title,
                    'url': list_or_empty(url),
                    'imgs': imgs,
                    'abstract': abstract,
                    'time': time
                },
                'gzh': {
                    'article_list_url': list_or_empty(gzh_article_url),
                    'headimage': list_or_empty((gzh_headimage)),
                    'name': list_or_empty(gzh_name),
                    'isv': list_or_empty(gzh_isv, int),
                }
            })
        return articles

    @staticmethod
    def get_article_by_history_json(text, article_json=None, **kwargs):
        if article_json is None:
            article_json = find_article_json_re.findall(text)
            article_json = article_json[0] + '}}]}'
            article_json = json.loads(article_json)

        biz = kwargs.get('biz', '')
        uin = kwargs.get('uin', '')
        key = kwargs.get('key', '')
        items = list()
        for listdic in article_json['list']:
            item = dict()
            comm_msg_info = listdic['comm_msg_info']
            item['send_id'] = comm_msg_info.get('id', '')  # 不可判重，一次群发的消息的id是一样的
            item['datetime'] = comm_msg_info.get('datetime', '')
            item['type'] = str(comm_msg_info.get('type', ''))
            if item['type'] == '1':
                # 文字
                item['content'] = comm_msg_info.get('content', '')
            elif item['type'] == '3':
                # 图片
                item[
                    'img_url'] = 'https://mp.weixin.qq.com/mp/getmediadata?__biz=' + biz + '&type=img&mode=small&msgid=' + \
                                 str(item['qunfa_id']) + '&uin=' + uin + '&key=' + key
            elif item['type'] == '34':
                # 音频
                item['play_length'] = listdic['voice_msg_ext_info'].get('play_length', '')
                item['fileid'] = listdic['voice_msg_ext_info'].get('fileid', '')
                item['audio_src'] = 'https://mp.weixin.qq.com/mp/getmediadata?__biz=' + biz + '&type=voice&msgid=' + \
                                    str(item['qunfa_id']) + '&uin=' + uin + '&key=' + key
            elif item['type'] == '49':
                # 图文
                app_msg_ext_info = listdic['app_msg_ext_info']
                url = app_msg_ext_info.get('content_url')
                url = replace_html(url)
                if url:
                    url = 'http://mp.weixin.qq.com' + url if 'http://mp.weixin.qq.com' not in url else url
                else:
                    url = ''
                item['main'] = 1
                item['title'] = app_msg_ext_info.get('title', '')
                item['digest'] = app_msg_ext_info.get('digest', '')
                item['fileid'] = app_msg_ext_info.get('fileid', '')
                item['content_url'] = url
                item['source_url'] = app_msg_ext_info.get('source_url', '')
                item['cover'] = app_msg_ext_info.get('cover', '')
                item['author'] = app_msg_ext_info.get('author', '')
                item['copyright_stat'] = app_msg_ext_info.get('copyright_stat', '')
                items.append(item)
                if app_msg_ext_info.get('is_multi', 0) == 1:
                    for multidic in app_msg_ext_info['multi_app_msg_item_list']:
                        url = multidic.get('content_url')
                        if url:
                            url = 'http://mp.weixin.qq.com' + url if 'http://mp.weixin.qq.com' not in url else url
                        else:
                            url = ''
                        itemnew = dict()
                        itemnew['qunfa_id'] = item['qunfa_id']
                        itemnew['datetime'] = item['datetime']
                        itemnew['type'] = item['type']
                        itemnew['main'] = 0
                        itemnew['title'] = multidic.get('title', '')
                        itemnew['digest'] = multidic.get('digest', '')
                        itemnew['fileid'] = multidic.get('fileid', '')
                        itemnew['content_url'] = url.replace('&amp;', '&')
                        itemnew['source_url'] = multidic.get('source_url', '')
                        itemnew['cover'] = multidic.get('cover', '')
                        itemnew['author'] = multidic.get('author', '')
                        itemnew['copyright_stat'] = multidic.get('copyright_stat', '')
                        items.append(itemnew)
                continue
            elif item['type'] == '62':
                item['cdn_videoid'] = listdic['video_msg_ext_info'].get('cdn_videoid', '')
                item['thumb'] = listdic['video_msg_ext_info'].get('thumb', '')
                item['video_src'] = 'https://mp.weixin.qq.com/mp/getcdnvideourl?__biz=' + biz + '&cdn_videoid=' + item[
                    'cdn_videoid'] + '&thumb=' + item['thumb'] + '&uin=' + uin + '&key=' + key
            items.append(item)

        items_new = []  # 删除搜狗本身携带的空数据
        for item in items:
            if (int(item['type']) == 49) and (not item['content_url']):
                pass
            else:
                items_new.append(item)
        return items_new

    @staticmethod
    def get_gzh_and_article_by_history(text):
        page = etree.HTML(text)
        profile_area = page.xpath('//div[@class="profile_info_area"]')[0]

        profile_img = profile_area.xpath('div[1]/span/img/@src')
        profile_name = profile_area.xpath('div[1]/div/strong/text()')
        profile_wechat_id = profile_area.xpath('div[1]/div/p/text()')
        profile_desc = profile_area.xpath('ul/li[1]/div/text()')
        profile_principal = profile_area.xpath('ul/li[2]/div/text()')

        return {
            'gzh_info': {
                'name': profile_name[0].strip(),
                'wechat_id': profile_wechat_id[0].replace('微信号: ', '').strip('\n'),
                'desc': profile_desc[0],
                'principal': profile_principal[0],
                'img': profile_img[0]
            },
            'article': WechatSogouStructuring.get_article_by_history_json(text)
        }

    def get_article_by_history(self, text):
        pass
