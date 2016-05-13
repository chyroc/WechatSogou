#coding=utf-8
import urllib.request
from lxml import etree
import myproxy
import requests
import re
import os
import json
import random
import sys
import time
import tempfile
from PIL import Image
from ruokuaicode import RClient


if sys.version_info < (3,):
    raise RuntimeError("at least Python3.0 is required!!")


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
        session: requests.session()对象
    """

    def __init__(self):
        self.cookiefile = 'cookie.dat'
        self.session = requests.session()
        if os.path.exists(self.cookiefile):
            with open(self.cookiefile) as f:
                cookie = json.load(f)
            self.session.cookies.update(cookie)
        self.agent = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
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
            "User-Agent": self.agent[1], #random.randint(0, len(self.agent) - 1)
            "Referer": referer if referer else 'http://weixin.sogou.com/',
            'Host': host if host else 'weixin.sogou.com',
        }
        if proxy:
            proip_http  = myproxy.get_one('http')
            proxies = {
                'http' : proip_http['http']+"://" + proip_http['ip'] + ":" + proip_http['duan'],
                'https' : proip_http['http'] + "://" + proip_http['ip'] + ":" + proip_http['duan']
            }
            r = self.session.get(url, headers=headers, proxies=proxies)
        else:
            r = self.session.get(url, headers=headers)
        if r.status_code == requests.codes.ok:
            r.encoding = self.__get_encoding_from_reponse(r)
            if '用户您好，您的访问过于频繁，为确认本次访问为正常用户行为，需要您协助验证' in r.text:
                self.vcode_url = url
                raise WechatSogouVcodeException('weixin.sogou.com verification code')
        else:
            raise WechatSogouRequestsException('requests status_code error', r.status_code)
        return r.text

    def __jiefeng(self, ruokuai=False):
        f = tempfile.TemporaryFile()
        codeurl = 'http://weixin.sogou.com/antispider/util/seccode.php?tc=' + str(time.time())[0:10]
        coder = self.session.get(codeurl)
        f.write(coder.content)
        if ruokuai:
            # todo
            img_code = ''
        else:
            im = Image.open(f)
            im.show()
            img_code = input("please input code: ")
        post_url = 'http://weixin.sogou.com/antispider/thank.php'
        post_data = {
            'c': img_code,
            'r': urllib.request.quote(self.vcode_url),
            'v': 5
        }
        headers = {
            "User-Agent": self.agent[1], #random.randint(0, len(self.agent) - 1)
            'Host': 'weixin.sogou.com',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2f'+urllib.request.quote(self.vcode_url.replace('http://',''))
        }
        rr = self.session.post(post_url, post_data, headers=headers)
        remsg = eval(rr.content)
        if remsg['code'] != 0:
            raise WechatSogouVcodeException('cannot jiefeng because '+ remsg['msg'])
        if hasattr(self, 'session'):
            with open(self.cookiefile, 'w') as f:
                json.dump(self.session.cookies.get_dict(), f)
        print(remsg['msg'])
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
        try:
            text = self.__get(request_url)
        except WechatSogouVcodeException:
            self.__jiefeng()
            text = self.__get(request_url, '', 'http://weixin.sogou.com/antispider/?from=%2f'+urllib.request.quote(self.vcode_url.replace('http://','')))
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
            {info:{img:'',name:'',wechatid:'',jieshao:'',zhuti:''},msgdict:''}
            img: 头像地址
            name: 公众号名称
            wechatid: 公众号id
            jieshao: 公众号介绍
            zhuti: 公众号主体信息
            msgdict: 最近文章信息字典
        """
        text = self.__get(url, 'mp.weixin.qq.com')
        page = etree.HTML(text)
        img = page.xpath('//div[@class="profile_info_area"]/div[@class="profile_info_group"]/span/img/@src')[0]
        info = page.xpath('//div[@class="profile_info_area"]/div[@class="profile_info_group"]/div')[0]
        info_list = self.__get_elem_text(info).split('微信号: ')
        jieshao = page.xpath('//div[@class="profile_info_area"]/ul')[0]
        jieshao_text = self.__get_elem_text(jieshao)
        jieshao_list = re.split('功能介绍|帐号主体', jieshao_text)
        msglist = re.findall("var msgList = '(.+?)';", text, re.S)[0]
        msgdict = eval(self.__replace_html(msglist))
        return {
            'info': {
                'img': img,
                'name': info_list[0],
                'wechatid': info_list[1],
                'jieshao': jieshao_list[1],
                'zhuti': jieshao_list[2]
            },
            'msgdict': msgdict
        }

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

    def deal_related(self, content_url, title):
        """获取文章相似文章

        Args:
            content_url: 文章地址
            title: 标题

        Returns:
            related_dict: 相似文章字典

        Raises:
            WechatSogouException: 错误信息errmsg
        """
        related_req_url = 'http://mp.weixin.qq.com/mp/getrelatedmsg?' \
                          'url=' + urllib.request.quote(content_url) \
                          + '&title=' + title \
                          + '&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=0&x5=0'
        related_text = self.__get(related_req_url, 'mp.weixin.qq.com', content_url)
        related_dict = eval(related_text)
        ret = related_dict['base_resp']['ret']
        errmsg = related_dict['base_resp']['errmsg'] if related_dict['base_resp']['errmsg'] else 'ret:' + str(ret)
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

    def get_recent_article_url_by_index_single(self, kind=0, page=0):
        """获取首页推荐文章公众号最近文章地址

        Args:
            kind: 类别，从0开始，经检测，至少应检查0-19，不保证之间每个都有
            page: 页数，从0开始

        Returns:
            recent_article_urls或者False
            recent_article_urls: 最近文章地址列表
            False: 该kind和page对应的页数没有文章
        """
        if page == 0:
            page_str = 'pc_0'
        else:
            page_str = str(page)
        url = 'http://weixin.sogou.com/pcindex/pc/pc_'+str(kind)+'/'+page_str+'.html'
        try:
            text = self.__get(url)
            page = etree.HTML(text)
            recent_article_urls = page.xpath('//li/div[@class="pos-wxrw"]/a/@href')
            return recent_article_urls
        except WechatSogouRequestsException as e:
            if e.status_code == 404:
                return False

    def get_recent_article_url_by_index_all(self):
        """获取首页推荐文章公众号最近文章地址，所有分类，所有页数

        Returns:
            return_urls: 最近文章地址列表
        """
        return_urls = []
        for i in range(20):
            j = 0
            urls = self.get_recent_article_url_by_index_single(i, j)
            while urls:
                return_urls.extend(urls)
                j += 1
                urls = self.get_recent_article_url_by_index_single(i, j)
        return return_urls

    def get_sugg(self, keyword):
        """获取微信搜狗搜索关键词联想

        Args:
            keyword: 关键词

        Returns:
            sugg: 联想关键词列表

        Raises:
            WechatSogouException: get_sugg keyword error 关键词不是str或者不是可以str()的类型
            WechatSogouException: sugg refind error 返回分析错误
        """
        try:
            keyword = str(keyword) if type(keyword) !=str else keyword
        except:
            raise WechatSogouException('get_sugg keyword error')
        url = 'http://w.sugg.sogou.com/sugg/ajaj_json.jsp?key='+keyword+'&type=wxpub&pr=web'
        text = self.__get(url, 'w.sugg.sogou.com')
        try:
            sugg = re.findall(r'\["'+keyword+'",(.*?),\["', text)[0]
            sugg = eval(sugg)
            return sugg
        except:
            raise WechatSogouException('sugg refind error')
