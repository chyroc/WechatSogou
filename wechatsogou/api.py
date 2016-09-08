# -*- coding: utf-8 -*-

import re
import time
from lxml import etree

from .basic import WechatSogouBasic
from .exceptions import *


class WechatSogouApi(WechatSogouBasic):
    """基于搜狗搜索的的微信公众号爬虫接口  接口类
    """

    def search_gzh_info(self, name, page=1):
        """搜索公众号

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
        text = self.search_gzh_text(name, page)
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
            cache = self.get_elem_text(info_instruction)
            cache = cache.replace('red_beg', '').replace('red_end', '')
            cache_list = cache.split('\n')
            cache_re = re.split('微信号：|功能介绍：|认证：|最近文章：', cache_list[0])
            name.append(cache_re[0])
            wechatid.append(cache_re[1])
            if "authnamewrite" in cache_re[2]:
                jieshao.append(re.sub("authnamewrite\('[0-9]'\)", "", cache_re[2]))
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
        """获取公众号微信号wechatid的信息

        因为wechatid唯一确定，所以第一个就是要搜索的公众号

        Args:
            wechatid: 公众号id

        Returns:
            字典{'name':name,'wechatid':wechatid,'jieshao':jieshao,'renzhen':renzhen,'qrcode':qrcodes,'img':img,'url':url}
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

    def search_article_info(self, name, page=1):
        """搜索文章

        Args:
            name: 搜索文章关键字
            page: 搜索的页数

        Returns:
            列表，每一项均是{'name','url','img','zhaiyao','gzhname','gzhqrcodes','gzhurl','time'}
            name: 文章标题
            url: 文章链接
            img: 文章封面图片缩略图，可转为高清大图
            zhaiyao: 文章摘要
            time: 文章推送时间，10位时间戳
            gzhname: 公众号名称
            gzhqrcodes: 公众号二维码
            gzhurl: 公众号最近文章地址

        """
        text = self.search_article_text(name, page)
        page = etree.HTML(text)
        img = list()
        info_imgs = page.xpath(u"//div[@class='wx-rb wx-rb3']/div[1]/a/img")
        for info_img in info_imgs:
            img.append(info_img.attrib['src'])
        url = list()
        info_urls = page.xpath(u"//div[@class='wx-rb wx-rb3']/div[2]/h4/a")
        for info_url in info_urls:
            url.append(info_url.attrib['href'])
        name = list()
        info_names = page.xpath(u"//div[@class='wx-rb wx-rb3']/div[2]/h4")
        for info_name in info_names:
            cache = self.get_elem_text(info_name)
            cache = cache.replace('red_beg', '').replace('red_end', '')
            name.append(cache)
        zhaiyao = list()
        info_zhaiyaos = page.xpath(u"//div[@class='wx-rb wx-rb3']/div[2]/p")
        for info_zhaiyao in info_zhaiyaos:
            cache = self.get_elem_text(info_zhaiyao)
            cache = cache.replace('red_beg', '').replace('red_end', '')
            zhaiyao.append(cache)
        gzhname = list()
        gzhqrcodes = list()
        gzhurl = list()
        info_gzhs = page.xpath(u"//div[@class='wx-rb wx-rb3']/div[2]/div/a")
        for info_gzh in info_gzhs:
            gzhname.append(info_gzh.attrib['title'])
            gzhqrcodes.append(info_gzh.attrib['data-encqrcodeurl'])
            gzhurl.append(info_gzh.attrib['href'])
        time = list()
        info_times = page.xpath(u"//div[@class='wx-rb wx-rb3']/div[2]/div/span/script/text()")
        for info_time in info_times:
            time.append(re.findall('vrTimeHandle552write\(\'(.*?)\'\)', info_time)[0])
        returns = list()
        for i in range(len(url)):
            returns.append(
                {
                    'name': name[i],
                    'url': url[i],
                    'img': img[i],
                    'zhaiyao': zhaiyao[i],
                    'gzhname': gzhname[i],
                    'gzhqrcodes': gzhqrcodes[i],
                    'gzhurl': gzhurl[i],
                    'time': time[i]
                }
            )
        return returns


    def get_gzh_recent_info(self, url):
        """最近文章页  公众号信息 和文章列表

        Args:
            url: 最近文章页地址

        Returns:
            字典{'gzh_info':gzh_info, 'articles':articles}

            gzh_info也是字典{'name':name,'wechatid':wechatid,'jieshao':jieshao,'renzhen':renzhen,'qrcode':qrcodes,'img':img,'url':url}
            name: 公众号名称
            wechatid: 公众号id
            jieshao: 介绍
            renzhen: 认证，为空表示未认证
            qrcode: 二维码
            img: 头像图片
            url: 最近文章地址

            articles列表，均是{'main':'', 'title':','digest':'','content':'','fileid':'','content_url':'','source_url':'','cover':'','author':'','copyright_stat':''}
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
        text = self.get_gzh_article_by_url_text(url)
        return {
            'gzh_info': self.get_gzh_article_gzh_by_url_dict(text, url),
            'articles': self.deal_gzh_article_dict(self.get_gzh_article_by_url_dict(text))
        }


    def get_gzh_article_by_wechatid_dict(self, wechatid):
        """获取微信号的最近文章

        Args:
            wechatid: 微信号

        Returns:
            列表，均是{'main':'', 'title':','digest':'','content':'','fileid':'','content_url':'','source_url':'','cover':'','author':'','copyright_stat':''}
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
        gzh = self.get_gzh_info(wechatid)
        if gzh:
            return self.get_gzh_article_and_gzh_by_url_dict(gzh['url'])
        return False

    def deal_related(self, article):
        """获取文章相似文章

        Args:
            article: 文章信息字典
            包含字典：article['content_url'],article['title'] 即可

        Returns:
            related_dict: 相似文章字典

        Raises:
            WechatSogouException: 错误信息errmsg
        """
        return super().deal_related(article)

    def deal_content(self, text):
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

    def deal_comment(self, text):
        """获取文章评论

        Args:
            text: 文章文本

        Returns:
            comment_dict: 评论字典

        Raises:
            WechatSogouException: 错误信息errmsg
        """
        sg_data = re.findall(r'window.sg_data={(.*?)}', text, re.S)
        sg_data = '{' + sg_data[0].replace(u'\r\n', '').replace(' ', '') + '}'
        sg_data = re.findall(r'{src:"(.*?)",ver:"(.*?)",timestamp:"(.*?)",signature:"(.*?)"}', sg_data)[0]
        comment_req_url = 'http://mp.weixin.qq.com/mp/getcomment?src=' + sg_data[0] + '&ver=' + sg_data[
            1] + '&timestamp=' + sg_data[2] + '&signature=' + sg_data[
                              3] + '&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=0&x5=0'
        comment_text = self.get(comment_req_url, 'mp.weixin.qq.com', 'http://mp.weixin.qq.com')
        comment_dict = eval(comment_text)
        ret = comment_dict['base_resp']['ret']
        errmsg = comment_dict['base_resp']['errmsg'] if comment_dict['base_resp']['errmsg'] else 'ret:' + str(ret)
        if ret != 0:
            raise WechatSogouException(errmsg)
        return comment_dict

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
        text = self.get_gzh_article_text(article['content_url'])
        yuan_url = re.findall('var msg_link = "(.*?)";', text)[0].replace('amp;', '')
        related = self.deal_related(article)
        comment = self.deal_comment(text)
        content_html, content_rich, content_text = self.deal_content(text)
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
        url = 'http://weixin.sogou.com/pcindex/pc/pc_' + str(kind) + '/' + page_str + '.html'
        try:
            text = self.get(url)
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
            keyword = str(keyword) if type(keyword) != str else keyword
        except:
            raise WechatSogouException('get_sugg keyword error')
        url = 'http://w.sugg.sogou.com/sugg/ajaj_json.jsp?key=' + keyword + '&type=wxpub&pr=web'
        text = self.get(url, 'w.sugg.sogou.com')
        try:
            sugg = re.findall(r'\["' + keyword + '",(.*?),\["', text)[0]
            sugg = eval(sugg)
            return sugg
        except:
            raise WechatSogouException('sugg refind error')
