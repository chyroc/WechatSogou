# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import re

from lxml import etree

from wechatsogou.tools import get_elem_text, list_or_empty


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

    def get_gzh_by_history(self, text):
        pass

    def get_article_by_history(self, text):
        pass
