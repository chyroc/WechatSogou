#coding=utf-8
import urllib.request
from lxml import etree
import myproxy
import requests
import re
import os
import json

class WechatSogouException(Exception):
    pass

class Session(object):
    def __init__(self):
        self.cookiefile = 'cookie.dat'

    def __enter__(self):
        self.session = requests.session()
        if os.path.exists(self.cookiefile):
            with open(self.cookiefile) as f:
                cookie = json.load(f)
            self.session.cookies.update(cookie)
            try:
                wechatspider().search_gzh('newsbro')
            except WechatSogouException:
                os.remove(self.cookiefile)
                self.session = requests.session()
                try:
                    wechatspider().search_gzh('newsbro')
                except WechatSogouException:
                    raise WechatSogouException('session test error')
        return self.session

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if hasattr(self, 'session'):
            with open(self.cookiefile, 'w') as f:
                json.dump(self.session.cookies.get_dict(), f)
        else:
            raise WechatSogouException('session empty cannot save')

class wechatspider(object):
    def __init__(self):
        self.cookiefile = 'cookie.dat'
        self.agent = [
            'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
        ]

    def __get_elem_text(self, elem):
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    def __get_encoding_from_reponse(self, r):
        encoding = requests.utils.get_encodings_from_content(r.text)
        if encoding:
            return encoding[0]
        else:
            return requests.utils.get_encoding_from_headers(r.headers)

    def get_session(self):
        with Session() as self.session:
            pass


    def __get(self, url, host='', referer=''):
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36',
            "Referer": referer if referer else 'http://weixin.sogou.com/',
            'Host': host if host else 'weixin.sogou.com',
        }
        # proip_http  = myproxy.get_one('http')
        # proip_https = myproxy.get_one('https')
        # proxies = {
        #     'http' : proip_http['http']+"://" + proip_http['ip'] + ":" + proip_http['duan'],
        #     'https' : proip_http['http'] + "://" + proip_http['ip'] + ":" + proip_http['duan']
        # }
        if hasattr(self, 'session'):
            req = self.session
        else:
            req = requests
        r = req.get(url, headers=headers)  #, proxies=proxies
        if r.status_code == requests.codes.ok:
            r.encoding = self.__get_encoding_from_reponse(r)
            if '用户您好，您的访问过于频繁，为确认本次访问为正常用户行为，需要您协助验证' in r.text:
                raise WechatSogouException('weixin.sogou.com verification code')
        else:
            raise WechatSogouException('requests status_code error')
        return r.text

    def __replace_html(self, s):
        s = s.replace('&quot;','"')
        s = s.replace('&amp;','&')
        s = s.replace('amp;','')
        s = s.replace('&lt;','<')
        s = s.replace('&gt;','>')
        s = s.replace('&nbsp;',' ')
        s = s.replace(r"\\", r'')
        return s

    def search_gzh(self, name, page=1):
        request_url = 'http://weixin.sogou.com/weixin?query='+name+'&_sug_type_=&_sug_=n&type=1&page='+str(page)+'&ie=utf8'
        text = self.__get(request_url)
        return text

    def search_gzh_info(self, name, page):
        text = self.search_gzh(name, page)
        page = etree.HTML(text)
        info_imgs = page.xpath(u"//div[@class='img-box']/img")
        img = list()
        for info_img in info_imgs:
            img.append(info_img.attrib['src'])
        info_urls = page.xpath(u"//div[@target='_blank']")
        url = list()
        for info_url in info_urls:
            url.append(info_url.attrib['href'])
        name = list()
        wechatid = list()
        jieshao = list()
        renzhen = list()
        info_instructions = page.xpath(u"//div[@class='txt-box']")
        for info_instruction in info_instructions:
            cache = self.__get_elem_text(info_instruction)
            cache = cache.replace('red_beg','').replace('red_end', '')
            cache_list = cache.split('\n')
            cache_re = re.split('微信号：|功能介绍：|认证：|最近文章：', cache_list[0])
            name.append(cache_re[0])
            wechatid.append(cache_re[1])
            if ".authnamewrite('2')" in cache_re[2]:
                jieshao.append(cache_re[2].replace(".authnamewrite('2')",''))
                renzhen.append(cache_re[3])
            else:
                jieshao.append(cache_re[2])
                renzhen.append('')
        qrcodes = list()
        info_qrcodes = page.xpath(u"//div[@class='pos-ico']/div/img")
        for info_qrcode in info_qrcodes:
            qrcodes.append(info_qrcode.attrib['src'])
        returns = list()
        for i in range(len(qrcodes)):
            returns.append(
                {
                    'name':name[i],
                     'wechatid':wechatid[i],
                     'jieshao':jieshao[i],
                     'renzhen':renzhen[i],
                     'qrcode':qrcodes[i],
                     'img':img[i],
                     'url':url[i]
                 }
            )
        return returns

    def get_gzh_info(self, wechatid):
        info = self.search_gzh_info(wechatid, 1)
        if info:
            return info[0]
        else:
            return False

    def get_gzh_article_dict(self, url):
        text = self.__get(url, 'mp.weixin.qq.com')
        msglist = re.findall("var msgList = '(.+?)';", text, re.S)[0]
        msgdict = eval(self.__replace_html(msglist))
        return msgdict

    def get_gzh_article_detail(self, msgdict):
        """
        省略了list->comm_msg_info,list->app_msg_ext_info->(subtype)
        """
        items = list()
        for listdic in msgdict['list']:
            item = listdic['app_msg_ext_info']
            items.append(
                {
                    'main': '1',
                    'title': item['title'],
                    'digest': item['digest'],
                    'content': item['content'],
                    'fileid': item['fileid'],
                    'content_url': 'http://mp.weixin.qq.com' + item['content_url'],
                    'source_url': item['source_url'],
                    'cover': item['cover'],
                    'author': item['author'],
                    'copyright_stat': item['copyright_stat']
                }
            )
            if item['is_multi'] == 1:
                for multidic in item['multi_app_msg_item_list']:
                    items.append(
                        {
                            'main': '0',
                            'title': multidic['title'],
                            'digest': multidic['digest'],
                            'content': multidic['content'],
                            'fileid': multidic['fileid'],
                            'content_url': 'http://mp.weixin.qq.com' + multidic['content_url'],
                            'source_url': multidic['source_url'],
                            'cover': multidic['cover'],
                            'author': multidic['author'],
                            'copyright_stat': multidic['copyright_stat']
                        }
                    )
        return items

    def __deal_comment(self, text):
        sg_data = re.findall(r'window.sg_data=(.*?)seajs', text, re.S)
        sg_data = sg_data[0].replace(u'\r\n','').replace(' ','')
        sg_data = re.findall(r'{src:"(.*?)",ver:"(.*?)",timestamp:"(.*?)",signature:"(.*?)"}', sg_data)[0]
        comment_req_url = 'http://mp.weixin.qq.com/mp/getcomment?src='+sg_data[0]+'&ver='+sg_data[1]+'&timestamp='+sg_data[2]+'&signature='+sg_data[3]+'&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=0&x5=0'
        comment_text = self.__get(comment_req_url, 'mp.weixin.qq.com', 'http://mp.weixin.qq.com')
        comment_dict = eval(comment_text)
        ret = comment_dict['base_resp']['ret']
        errmsg = comment_dict['base_resp']['errmsg']
        if ret != 0:
            raise WechatSogouException(errmsg)
        return comment_dict

    def __deal_related(self, article):
        content_url = article['content_url']
        title = article['title']
        related_req_url = 'http://mp.weixin.qq.com/mp/getrelatedmsg?' \
                          'url=' + urllib.request.quote(content_url) \
                          + '&title=' + title \
                          + '&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=0&x5=0'
        related_text = self.__get(related_req_url, 'mp.weixin.qq.com', content_url)
        related_dict = eval(related_text)
        ret = related_dict['base_resp']['ret']
        errmsg = related_dict['base_resp']['errmsg'] if related_dict['base_resp']['errmsg'] else 'ret:'+str(ret)
        if ret != 0:
            print(related_dict)
            raise WechatSogouException(errmsg)
        return related_dict
    def __deal_content(self, text):
        content_html = re.findall(r'<div class="rich_media_content " id="js_content">(.*?)</div>', text, re.S)[0]
        content_rich = re.sub(r'<(?!img|br).*?>', '', content_html)
        pipei = re.compile(r'<img(.*?)src="(.*?)"(.*?)/>')
        content_text = pipei.sub(lambda m: '<img src="' + m.group(2) + '" />', content_rich)
        return content_html, content_rich, content_text
    def get_get_gzh_article_info(self, article):
        content_url = article['content_url']
        text = self.__get(content_url, 'mp.weixin.qq.com')
        yuan_url = re.findall('var msg_link = "(.*?)";', text)[0].replace('amp;','')
        related = self.__deal_related(article)
        comment = self.__deal_comment(text)
        content_html, content_rich, content_text = self.__deal_content(text)
        return {
            'yuan': yuan_url,
            'related': related,
            'comment': comment,
            'content': {
                'content_html': content_html,
                'content_rich': content_rich,
                'content_text': content_text
            }
        }
