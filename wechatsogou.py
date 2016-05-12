#coding=utf-8
import urllib.request
from lxml import etree
import myproxy
import requests
import re
import os
import json
import random

class WechatSogouException(Exception):
    """基于搜狗的微信公众号爬虫异常类
    """
    pass

class WechatSogouVcodeException(WechatSogouException):
    """基于搜狗的微信公众号爬虫 出现验证码 异常类
    """
    pass

class WechatSogouRequestsException(WechatSogouException):
    """基于搜狗的微信公众号爬虫 抓取 异常类
    """
    def __init__(self, errmsg, status_code):
        WechatSogouException(errmsg)
        self.status_code = status_code

class WechatSpider(object):
    """基于搜狗的微信公众号爬虫类

    Attributes:
        agent: 模拟浏览器头
    """

    def __init__(self):
        self.cookiefile = 'cookie.dat'
        self.agent = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
        ]

    def __get_elem_text(self, elem):
        """抽取lxml.etree库中elem对象中文字

        Args:
            elem: lxml.etree库中elem对象

        Returns:
            elem中文字
        """
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    def __get_encoding_from_reponse(self, r):
        """获取requests库get或post返回的对象编码

        Args:
            r: requests库get或post返回的对象

        Returns:
            对象编码
        """
        encoding = requests.utils.get_encodings_from_content(r.text)
        return encoding[0] if encoding else requests.utils.get_encoding_from_headers(r.headers)

    def __get(self, url, host='', referer='', proxy=False):
        """封装request库get方法

        Args:
            url: 请求url
            host: 请求host
            referer: 请求referer
            proxy: 是否启用代理请求

        Returns:
            text: 请求url的网页内容

        Raises:
            WechatSogouException: 操作频繁以致出现验证码或requests请求返回码错误
        """
        headers = {
            "User-Agent": self.agent[random.randint(0, len(self.agent) - 1)],
            "Referer": referer if referer else 'http://weixin.sogou.com/',
            'Host': host if host else 'weixin.sogou.com',
        }
        if proxy:
            proip_http  = myproxy.get_one('http')
            proip_https = myproxy.get_one('https')
            proxies = {
                'http' : proip_http['http']+"://" + proip_http['ip'] + ":" + proip_http['duan'],
                'https' : proip_http['http'] + "://" + proip_http['ip'] + ":" + proip_http['duan']
            }
            r = requests.get(url, headers=headers, proxies=proxies)
        else:
            r = requests.get(url, headers=headers)
        if r.status_code == requests.codes.ok:
            r.encoding = self.__get_encoding_from_reponse(r)
            if '用户您好，您的访问过于频繁，为确认本次访问为正常用户行为，需要您协助验证' in r.text:
                #raise WechatSogouException('weixin.sogou.com verification code')
                raise WechatSogouException('weixin.sogou.com verification code')
        else:
            raise WechatSogouRequestsException('requests status_code error', r.status_code)
        return r.text

    def __replace_html(self, s):
        """替换html‘&quot;’等转义内容为正常内容

        Args:
            s: 文字内容

        Returns:
            s: 处理反转义后的文字
        """
        s = s.replace('&quot;','"')
        s = s.replace('&amp;','&')
        s = s.replace('amp;','')
        s = s.replace('&lt;','<')
        s = s.replace('&gt;','>')
        s = s.replace('&nbsp;',' ')
        s = s.replace(r"\\", r'')
        return s

    def search_gzh(self, name, page=1):
        """通过搜狗搜索获取关键字返回的文本

        Args:
            name: 搜索关键字
            page: 搜索的页数

        Returns:
            text: 返回的文本
        """
        request_url = 'http://weixin.sogou.com/weixin?query='+urllib.request.quote(name)+'&_sug_type_=&_sug_=n&type=1&page='+str(page)+'&ie=utf8'
        text = self.__get(request_url)
        return text

    def search_gzh_info(self, name, page):
        """对搜索的文本进行处理

        Args:
            name: 搜索关键字
            page: 搜索的页数

        Returns:
            列表，每一项均是{'name':name,'wechatid':wechatid,'jieshao':jieshao,'renzhen':renzhen,'qrcode':qrcodes,'img':img,'url':url}
            name: 公众号名称
            wechatid: 公众号id
            jieshao: 介绍
            renzhen: 认证，为空表示未认证
            qrcode: 二维码
            img: 头像图片
            url: 最近文章地址
        """
        text = self.search_gzh(name, page)
        page = etree.HTML(text)
        img = list()
        info_imgs = page.xpath(u"//div[@class='img-box']/img")
        for info_img in info_imgs:
            img.append(info_img.attrib['src'])
        url = list()
        info_urls = page.xpath(u"//div[@target='_blank']")
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
                    'name': name[i],
                    'wechatid': wechatid[i],
                    'jieshao': jieshao[i],
                    'renzhen': renzhen[i],
                    'qrcode': qrcodes[i],
                    'img': img[i],
                    'url': url[i]
                }
            )
        return returns

    def get_gzh_info(self, wechatid):
        """通过wechatid获取公众号信息，因为

        因为wechatid唯一确定，所以第一个就是要搜索的公众号

        Args:
            wechatid: 公众号id

        Returns:
            {'name':name,'wechatid':wechatid,'jieshao':jieshao,'renzhen':renzhen,'qrcode':qrcodes,'img':img,'url':url}
            name: 公众号名称
            wechatid: 公众号id
            jieshao: 介绍
            renzhen: 认证，为空表示未认证
            qrcode: 二维码
            img: 头像图片
            url: 最近文章地址
        """
        info = self.search_gzh_info(wechatid, 1)
        return info[0] if info else False

    def get_gzh_article_dict(self, url):
        """获取公众号最近文章页信息

        Args:
            url: 最近文章页地址

        Returns:
            msgdict: 最近文章信息字典
        """
        text = self.__get(url, 'mp.weixin.qq.com')
        msglist = re.findall("var msgList = '(.+?)';", text, re.S)[0]
        msgdict = eval(self.__replace_html(msglist))
        return msgdict

    def get_gzh_article_detail(self, msgdict):
        """处理最近文章页信息

        Args:
            msgdict: 最近文章信息字典

        Returns:
            {'main':'', 'title':','digest':'','content':'','fileid':'','content_url':'','source_url':'','cover':'','author':'','copyright_stat':''}
            main: 是否是一次推送中第一篇文章，1则是
            title: 文章标题
            digest: 摘要
            content:
            fileid:
            content_url: 文章地址
            source_url: 原文地址
            cover: 封面图片
            author: 作者
            copyright_stat: 文章内容版权性
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
        """获取文章评论

        Args:
            text: 使用content_url获取的文章文本

        Returns:
            comment_dict: 评论字典

        Raises:
            WechatSogouException: 错误信息errmsg
        """
        sg_data = re.findall(r'window.sg_data=(.*?)seajs', text, re.S)
        sg_data = sg_data[0].replace(u'\r\n','').replace(' ','')
        sg_data = re.findall(r'{src:"(.*?)",ver:"(.*?)",timestamp:"(.*?)",signature:"(.*?)"}', sg_data)[0]
        comment_req_url = 'http://mp.weixin.qq.com/mp/getcomment?src='+sg_data[0]+'&ver='+sg_data[1]+'&timestamp='+sg_data[2]+'&signature='+sg_data[3]+'&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=0&x5=0'
        comment_text = self.__get(comment_req_url, 'mp.weixin.qq.com', 'http://mp.weixin.qq.com')
        comment_dict = eval(comment_text)
        ret = comment_dict['base_resp']['ret']
        errmsg = comment_dict['base_resp']['errmsg'] if comment_dict['base_resp']['errmsg'] else 'ret:' + str(ret)
        if ret != 0:
            raise WechatSogouException(errmsg)
        return comment_dict

    def __deal_related(self, article):
        """获取文章相似文章

        Args:
            article: 文章信息字典

        Returns:
            related_dict: 相似文章字典

        Raises:
            WechatSogouException: 错误信息errmsg
        """
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
            raise WechatSogouException(errmsg)
        return related_dict

    def __deal_content(self, text):
        """获取文章内容

        Args:
            text: 文章页文本

        Returns:
            content_html, content_rich, content_text
            content_html: 原始文章内容，包括html标签及样式
            content_rich: 包含图片（包括图片应展示的样式）的文章内容
            content_text: 包含图片（`<img src="..." />`格式）的文章内容
        """
        content_html = re.findall(r'<div class="rich_media_content " id="js_content">(.*?)</div>', text, re.S)[0]
        content_rich = re.sub(r'<(?!img|br).*?>', '', content_html)
        pipei = re.compile(r'<img(.*?)src="(.*?)"(.*?)/>')
        content_text = pipei.sub(lambda m: '<img src="' + m.group(2) + '" />', content_rich)
        return content_html, content_rich, content_text

    def get_gzh_article_info(self, article):
        """获取文章详情

        Args:
            article: 文章信息字典

        Returns:
            {'yuan':'','related':'','comment':'','content': {'content_html':'','content_rich':'','content_text':''}
            yuan: 文章固定地址
            related: 相似文章信息字典
            comment: 评论信息字典
            content: 文章内容
        """
        text = self.__get(article['content_url'], 'mp.weixin.qq.com')
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
    def get_recent_article_url_by_index_single(self):
        url = 'http://weixin.sogou.com/pcindex/pc/pc_23/pc_23.html'
        try:
            text = self.__get(url)
        except WechatSogouRequestsException as e:
            print(e.status_code)
            exit()
        page = etree.HTML(text)
        recent_article_urls = page.xpath('//li/div[@class="pos-wxrw"]/a/@href')
        return recent_article_urls
