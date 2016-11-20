# -*- coding: utf-8 -*-

import re
import requests
import time
from lxml import etree

from .basic import WechatSogouBasic
from .exceptions import *

import logging

logger = logging.getLogger()


class WechatSogouApi(WechatSogouBasic):
    """基于搜狗搜索的的微信公众号爬虫接口  接口类
    """

    def __init__(self, **kwargs):
        super(WechatSogouApi, self).__init__(**kwargs)

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
        text = self._search_gzh_text(name, page)
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
            cache = self._get_elem_text(info_instruction)
            cache = cache.replace('red_beg', '').replace('red_end', '')
            cache_list = cache.split('\n')
            cache_re = re.split(u'微信号：|功能介绍：|认证：|最近文章：', cache_list[0])
            name.append(cache_re[0])
            wechatid.append(cache_re[1])
            for i in range(4 - len(cache_re)):
                cache_re.append('')
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
        text = self._search_article_text(name, page)
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
            cache = self._get_elem_text(info_name)
            cache = cache.replace('red_beg', '').replace('red_end', '')
            name.append(cache)
        zhaiyao = list()
        info_zhaiyaos = page.xpath(u"//div[@class='wx-rb wx-rb3']/div[2]/p")
        for info_zhaiyao in info_zhaiyaos:
            cache = self._get_elem_text(info_zhaiyao)
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

    def get_gzh_message(self, **kwargs):
        """解析最近文章页  或  解析历史消息记录

        Args:
            ::param url 最近文章地址
            ::param wechatid 微信号
            ::param wechat_name 微信昵称(不推荐，因为不唯一)

            最保险的做法是提供url或者wechatid

        Returns:
            gzh_messages 是 列表，每一项均是字典，一定含有字段qunfa_id,datetime,type
            当type不同时，含有不同的字段，具体见文档
        """
        url = kwargs.get('url', None)
        wechatid = kwargs.get('wechatid', None)
        wechat_name = kwargs.get('wechat_name', None)
        if url:
            text = self._get_gzh_article_by_url_text(url)
        elif wechatid:
            gzh_info = self.get_gzh_info(wechatid)
            url = gzh_info['url']
            text = self._get_gzh_article_by_url_text(url)
        elif wechat_name:
            gzh_info = self.get_gzh_info(wechat_name)
            url = gzh_info['url']
            text = self._get_gzh_article_by_url_text(url)
        else:
            raise WechatSogouException('get_gzh_recent_info need param text and url')

        return self._deal_gzh_article_dict(self._get_gzh_article_by_url_dict(text))

    def get_gzh_message_and_info(self, **kwargs):
        """最近文章页  公众号信息 和 群发信息

        Args:
            ::param url 最近文章地址
            ::param wechatid 微信号
            ::param wechat_name 微信昵称(不推荐，因为不唯一)

            最保险的做法是提供url或者wechatid

        Returns:
            字典{'gzh_info':gzh_info, 'gzh_messages':gzh_messages}

            gzh_info 也是字典{'name':name,'wechatid':wechatid,'jieshao':jieshao,'renzhen':renzhen,'qrcode':qrcodes,'img':img,'url':url}
            name: 公众号名称
            wechatid: 公众号id
            jieshao: 介绍
            renzhen: 认证，为空表示未认证
            qrcode: 二维码
            img: 头像图片
            url: 最近文章地址

            gzh_messages 是 列表，每一项均是字典，一定含有字段qunfa_id,datetime,type
            当type不同时，含有不同的字段，具体见文档
        """
        url = kwargs.get('url', None)
        wechatid = kwargs.get('wechatid', None)
        wechat_name = kwargs.get('wechat_name', None)
        if url:
            text = self._get_gzh_article_by_url_text(url)
        elif wechatid:
            gzh_info = self.get_gzh_info(wechatid)
            url = gzh_info['url']
            text = self._get_gzh_article_by_url_text(url)
        elif wechat_name:
            gzh_info = self.get_gzh_info(wechat_name)
            url = gzh_info['url']
            text = self._get_gzh_article_by_url_text(url)
        else:
            raise WechatSogouException('get_gzh_recent_info need param text and url')

        return {
            'gzh_info': self._get_gzh_article_gzh_by_url_dict(text, url),
            'gzh_messages': self._deal_gzh_article_dict(self._get_gzh_article_by_url_dict(text))
        }

    def deal_article_content(self, **kwargs):
        """获取文章内容

        Args:
            ::param url 文章页 url
            ::param text 文章页 文本

        Returns:
            content_html, content_rich, content_text
            content_html: 原始文章内容，包括html标签及样式
            content_rich: 包含图片（包括图片应展示的样式）的文章内容
            content_text: 包含图片（`<img src="..." />`格式）的文章内容
        """
        url = kwargs.get('url', None)
        text = kwargs.get('text', None)

        if text:
            pass
        elif url:
            text = self._get_gzh_article_text(url)
        else:
            raise WechatSogouException('deal_content need param url or text')

        content_html = re.findall(u'<div class="rich_media_content " id="js_content">(.*?)</div>', text, re.S)[0]
        # content_rich = re.sub(u'<(?!img|br).*?>', '', content_html)
        # pipei = re.compile(u'<img(.*?)src="(.*?)"(.*?)/>')
        # content_text = pipei.sub(lambda m: '<img src="' + m.group(2) + '" />', content_rich)
        return content_html

    def deal_article_related(self, url, title):
        """获取文章相似文章

        Args:
            url: 文章链接
            title: 文章标题

        Returns:
            related_dict: 相似文章字典

        Raises:
            WechatSogouException: 错误信息errmsg
        """
        return self._deal_related(url, title)

    def deal_article_comment(self, **kwargs):
        """获取文章评论

        Args:
            text: 文章文本

        Returns:
            comment_dict: 评论字典

        Raises:
            WechatSogouException: 错误信息errmsg
        """
        url = kwargs.get('url', None)
        text = kwargs.get('text', None)

        if text:
            pass
        elif url:
            text = self._get_gzh_article_text(url)
        else:
            raise WechatSogouException('deal_content need param url or text')

        sg_data = re.findall(u'window.sg_data={(.*?)}', text, re.S)
        sg_data = '{' + sg_data[0].replace(u'\r\n', '').replace(' ', '') + '}'
        sg_data = re.findall(u'{src:"(.*?)",ver:"(.*?)",timestamp:"(.*?)",signature:"(.*?)"}', sg_data)[0]
        comment_req_url = 'http://mp.weixin.qq.com/mp/getcomment?src=' + sg_data[0] + '&ver=' + sg_data[
            1] + '&timestamp=' + sg_data[2] + '&signature=' + sg_data[
                              3] + '&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=0&x5=0'
        comment_text = self._get(comment_req_url, 'get', host='mp.weixin.qq.com', referer='http://mp.weixin.qq.com')
        comment_dict = eval(comment_text)
        ret = comment_dict['base_resp']['ret']
        errmsg = comment_dict['base_resp']['errmsg'] if comment_dict['base_resp']['errmsg'] else 'ret:' + str(ret)
        if ret != 0:
            logger.error(errmsg)
            raise WechatSogouException(errmsg)
        return comment_dict

    def deal_article_yuan(self, **kwargs):
        url = kwargs.get('url', None)
        text = kwargs.get('text', None)

        if text:
            pass
        elif url:
            text = self._get_gzh_article_text(url)
        else:
            raise WechatSogouException('deal_article_yuan need param url or text')
        try:
            yuan = re.findall('var msg_link = "(.*?)";', text)[0].replace('amp;', '')
        except IndexError as e:
            if '系统出错' in text:
                logger.debug('系统出错 - 链接问题，正常')
            elif '此内容因违规无法查看' in text:
                logger.debug('此内容因违规无法查看 - 剔除此类文章')
            else:
                logger.error(e)

                if url:
                    logger.error(url)
                else:
                    title = re.findall('<title>(.*?)</title>', text)
                    if title:
                        logger.error(title[0])
                    else:
                        logger.error(text)

            raise WechatSogouBreakException()

        return yuan

    def deal_article(self, url, title=None):
        """获取文章详情

        Args:
            url: 文章链接
            title: 文章标题
            注意，title可以为空，则表示不根据title获取相似文章

        Returns:
            {'yuan':'','related':'','comment':'','content': {'content_html':'','content_rich':'','content_text':''}
            yuan: 文章固定地址
            related: 相似文章信息字典
            comment: 评论信息字典
            content: 文章内容
        """
        text = self._get_gzh_article_text(url)
        yuan_url = re.findall('var msg_link = "(.*?)";', text)[0].replace('amp;', '')

        comment = self.deal_article_comment(text=text)
        content_html = self.deal_article_content(text=text)
        retu = {
            'yuan': yuan_url,
            'comment': comment,
            'content_html': content_html
        }

        if title is not None:
            related = self.deal_article_related(url, title)
            retu['related'] = related
            return retu
        else:
            return retu

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
            text = self._get(url)
            page = etree.HTML(text)
            recent_article_urls = page.xpath('//li/div[@class="pos-wxrw"]/a/@href')
            reurls = []
            for reurl in recent_article_urls:
                if 'mp.weixin.qq.com' in reurl:
                    reurls.append(reurl)
            return reurls
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
        except Exception as e:
            logger.error('get_sugg keyword error', e)
            raise WechatSogouException('get_sugg keyword error')
        url = 'http://w.sugg.sogou.com/sugg/ajaj_json.jsp?key=' + keyword + '&type=wxpub&pr=web'
        text = self._get(url, 'get', host='w.sugg.sogou.com')
        try:
            sugg = re.findall(u'\["' + keyword + '",(.*?),\["', text)[0]
            sugg = eval(sugg)
            return sugg
        except Exception as e:
            logger.error('sugg refind error', e)
            raise WechatSogouException('sugg refind error')

    def deal_mass_send_msg(self, url, wechatid):
        """解析 历史消息

        ::param url是抓包获取的历史消息页
        """
        session = requests.session()
        r = session.get(url, verify=False)
        if r.status_code == requests.codes.ok:
            try:
                biz = re.findall('biz = \'(.*?)\',', r.text)[0]
                key = re.findall('key = \'(.*?)\',', r.text)[0]
                uin = re.findall('uin = \'(.*?)\',', r.text)[0]
                pass_ticket = self._get_url_param(url).get('pass_ticket', [''])[0]

                self._uinkeybiz(wechatid, uin, key, biz, pass_ticket, 0)
                self._cache_history_session(wechatid, session)

            except IndexError:
                logger.error('deal_mass_send_msg error. maybe you should get the mp url again')
                raise WechatSogouHistoryMsgException('deal_mass_send_msg error. maybe you should get the mp url again')
        else:
            logger.error('requests status_code error', r.status_code)
            raise WechatSogouRequestsException('requests status_code error', r.status_code)

    def deal_mass_send_msg_page(self, wechatid, updatecache=True):
        url = 'http://mp.weixin.qq.com/mp/getmasssendmsg?'
        uin, key, biz, pass_ticket, frommsgid = self._uinkeybiz(wechatid)
        print([uin, key, biz, pass_ticket, frommsgid])
        url = url + 'uin=' + uin + '&'
        url = url + 'key=' + key + '&'
        url = url + '__biz=' + biz + '&'
        url = url + 'pass_ticket=' + pass_ticket + '&'
        url = url + 'frommsgid=' + str(frommsgid) + '&'
        data = {
            'f': 'json',
            'count': '10',
            'wxtoken': '',
            'x5': '0'
        }
        for k, v in data.items():
            url = url + k + '=' + v + '&'
        url = url[:-1]
        # print(url)

        try:
            session = self._cache_history_session(wechatid)
            r = session.get(url, headers={'Host': 'mp.weixin.qq.com'}, verify=False)
            rdic = eval(r.text)
            if rdic['ret'] == 0:

                data_dict_from_str = self._str_to_dict(rdic['general_msg_list'])

                if rdic['is_continue'] == 0 and rdic['count'] == 0:
                    raise WechatSogouEndException()

                msg_dict = self._deal_gzh_article_dict(data_dict_from_str)
                msg_dict_new = reversed(msg_dict)
                msgid = 0
                for m in msg_dict_new:
                    if int(m['type']) == 49:
                        msgid = m['qunfa_id']
                        break

                if updatecache:
                    self._uinkeybiz(wechatid, rdic['uin_code'], rdic['key'], rdic['bizuin_code'], pass_ticket, msgid)

                return msg_dict
            else:
                logger.error('deal_mass_send_msg_page ret ' + str(rdic['ret']) + ' errmsg ' + rdic['errmsg'])
                raise WechatSogouHistoryMsgException(
                    'deal_mass_send_msg_page ret ' + str(rdic['ret']) + ' errmsg ' + rdic['errmsg'])
        except AttributeError:
            logger.error('deal_mass_send_msg_page error, please delete cache file')
            raise WechatSogouHistoryMsgException('deal_mass_send_msg_page error, please delete cache file')
