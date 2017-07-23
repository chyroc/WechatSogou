# -*- coding: utf-8 -*-

import re
import logging

import requests
from lxml import etree

from .basic import WechatSogouBasic
from .exceptions import (
    WechatSogouException,
    WechatSogouEndException,
    WechatSogouBreakException,
    WechatSogouRequestsException,
    WechatSogouHistoryMsgException
)
from .tools import (
    get_elem_text,
    list_or_empty
)

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
        lis = page.xpath('//ul[@class="news-list2"]/li')
        relist = []
        for li in lis:
            url = li.xpath('div/div[1]/a/@href')
            img = li.xpath('div/div[1]/a/img/@src')
            name = get_elem_text(li.xpath('div/div[2]/p[1]')[0])
            info = get_elem_text(li.xpath('div/div[2]/p[2]')[0])
            info = re.split('微信号:|月发文|篇|平均阅读', info)
            try:
                wechatid = info[1]
            except IndexError:
                wechatid = ''
            try:
                post_perm = int(info[2])
            except IndexError:
                post_perm = 0
            try:
                read_count = int(info[4])
            except IndexError:
                read_count = 0
            qrcode = li.xpath('div/div[3]/span/img[1]/@src')
            jieshao = get_elem_text(li.xpath('dl[1]/dd')[0])
            renzhen = li.xpath('dl[2]/dd/text()')
            relist.append({
                'url': url[0],
                'img': img[0],
                'name': name.replace('red_beg', '').replace('red_end', ''),
                'wechatid': wechatid,
                'post_perm': post_perm,
                'read_count': read_count,
                'qrcode': qrcode[0] if qrcode else '',
                'introduction': jieshao.replace('red_beg', '').replace('red_end', ''),
                'authentication': renzhen[0] if renzhen else ''
            })
        return relist

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
        articles = []
        lis = page.xpath('//ul[@class="news-list"]/li')
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
            gzh_qrcodeurl = gzh_info.xpath('@data-encqrcodeurl')
            gzh_name = gzh_info.xpath('@data-sourcename')
            gzh_wechatid = gzh_info.xpath('@data-username')
            gzh_isv = gzh_info.xpath('@data-isv')
            gzh_avgpublish = gzh_info.xpath('@data-avgpublish')
            gzh_avgread = gzh_info.xpath('@data-avgread')

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
                    'qrcodeurl': list_or_empty((gzh_qrcodeurl)),
                    'name': list_or_empty(gzh_name),
                    'wechatid': list_or_empty(gzh_wechatid),
                    'isv': list_or_empty(gzh_isv, int),
                    'avgpublish': list_or_empty(gzh_avgpublish, int),
                    'avgread': list_or_empty(gzh_avgread, int)
                }
            })
        return articles

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
        comment_req_url = 'http://mp.weixin.qq.com/mp/getcomment?src={}&ver={}&timestamp={}&signature={}&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=0&x5=0'.format(
            *sg_data)
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

        comment = self.deal_article_comment(text=text)
        content_html = self.deal_article_content(text=text)
        retu = {
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
            r = requests.get(url)
            r.encoding = 'utf-8'
            text = r.text
            page = etree.HTML(text)
            lis = page.xpath('//ul[@class="news-list"]/li')
            reurls = []
            for li in lis:
                url = li.xpath('div[1]/a/@href')
                img = li.xpath('div[1]/a/img/@src')
                title = li.xpath('div[2]/h3/a/text()')
                time = li.xpath('div[2]/div/@t')
                gzh_name = li.xpath('div[2]/div/a/text()')
                gzh_article_list_url = li.xpath('div[2]/div/a/@href')
                reurls.append({
                    'url': list_or_empty(url),
                    'img': list_or_empty(img),
                    'title': list_or_empty(title),
                    'time': list_or_empty(time, int),
                    'gzh_name': list_or_empty(gzh_name),
                    'gzh_article_list_url': list_or_empty(gzh_article_list_url)
                })
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
