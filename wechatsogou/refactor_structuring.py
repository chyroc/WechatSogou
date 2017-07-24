# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

from lxml import etree

from wechatsogou.tools import get_elem_text


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

    def get_article_by_search(self, text):
        pass

    def get_gzh_by_history(self, text):
        pass

    def get_article_by_history(self, text):
        pass
