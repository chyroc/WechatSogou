# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import time

import requests

from wechatsogou.exceptions import WechatSogouRequestsException, WechatSogouVcodeOcrException
from wechatsogou.request import WechatSogouRequest
from wechatsogou.structuring import WechatSogouStructuring
from wechatsogou.identify_image import (
    ws_cache,
    identify_image_callback_example,
    deblocking_callback_search_example,
    deblocking_callback_history_example)


class WechatSogouAPI(object):
    def __set_cookie(self, suv=None, snuid=None, referer=None):
        suv = ws_cache.get('suv') if suv is None else suv
        snuid = ws_cache.get('snuid') if snuid is None else snuid

        return {'Cookie': 'SUV={};SNUID={};'.format(suv, snuid)} if referer is None else {
            'Cookie': 'SUV={};SNUID={};'.format(suv, snuid), 'Referer': referer}

    def __set_cache(self, suv, snuid):
        ws_cache.set('suv', suv)
        ws_cache.set('snuid', snuid)

    def __deblocking_search(self, url, resp, req, deblocking_callback, identify_image_callback):
        millis = int(round(time.time() * 1000))
        r_img = req.get('http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(millis))
        if not r_img.ok:
            raise WechatSogouRequestsException('WechatSogouAPI get img', resp)

        if callable(deblocking_callback):
            r_deblocking = deblocking_callback(req, resp, r_img.content)
        else:
            identify_image_callback = identify_image_callback if callable(
                identify_image_callback) else identify_image_callback_example
            r_deblocking = deblocking_callback_search_example(url, req, resp, r_img.content, identify_image_callback)

        if r_deblocking['code'] != 0:
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {code}, msg: {msg}'.format(**r_deblocking))
        else:
            self.__set_cache(req.cookies.get('SUID'), r_deblocking['id'])

    def __deblocking_history(self, url, resp, req, deblocking_callback, identify_image_callback):
        r_img = req.get('https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(time.time() * 1000))
        if not r_img.ok:
            raise WechatSogouRequestsException('WechatSogouAPI deblocking_history get img', resp)

        if callable(deblocking_callback):
            r_deblocking = deblocking_callback(req, resp, r_img.content)
        else:
            identify_image_callback = identify_image_callback if callable(
                identify_image_callback) else identify_image_callback_example
            r_deblocking = deblocking_callback_history_example(url, req, resp, r_img.content, identify_image_callback)

        if r_deblocking['ret'] != 0:
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {ret}, msg: {errmsg}, cookie_count: {cookie_count}'.format(
                    **r_deblocking))

    def get_gzh_info(self, wecgat_id_or_name, deblocking_callback=None, identify_image_callback=None):
        """获取公众号微信号 wechatid 的信息

        因为wechatid唯一确定，所以第一个就是要搜索的公众号

        Parameters
        ----------
        wecgat_id_or_name : str or unicode
            wechat_id or wechat_name
        deblocking_callback : callable
            处理出现验证码页面的函数，参见 deblocking_callback_example
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        dict or None
            {
                'profile_url': '',  # 最近10条群发页链接
                'headimage': '',  # 头像
                'wechat_name': '',  # 名称
                'wechat_id': '',  # 微信id
                'post_perm': '',  # 最近一月群发数
                'qrcode': '',  # 二维码
                'introduction': '',  # 介绍
                'authentication': ''  # 认证
            }
        """
        info = self.search_gzh(wecgat_id_or_name)
        return info[0] if info else None

    def search_gzh(self, keyword, page=1, deblocking_callback=None, identify_image_callback=None):
        """搜索 公众号

        对于出现验证码的情况，可以由使用者自己提供：
            1、函数 deblocking_callback ，这个函数 handle 出现验证码到解决的整个流程
            2、也可以 只提供函数 identify_image_callback，这个函数输入验证码二进制数据，输出验证码文字，剩下的由 wechatsogou 包来解决
        注意：
            函数 deblocking_callback 和 identify_image_callback 只需要提供一个，如果都提供了，那么 identify_image_callback 不起作用

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1
        deblocking_callback : callable
            处理出现验证码页面的函数，参见 deblocking_callback_example
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        list[dict]
            {
                'profile_url': '',  # 最近10条群发页链接
                'headimage': '',  # 头像
                'wechat_name': '',  # 名称
                'wechat_id': '',  # 微信id
                'post_perm': '',  # 最近一月群发数
                'qrcode': '',  # 二维码
                'introduction': '',  # 介绍
                'authentication': ''  # 认证
            }

        Raises
        ------
        WechatSogouRequestsException
            requests error
        """
        req = requests.session()

        url = WechatSogouRequest.gen_search_gzh_url(keyword, page)
        resp = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie())

        if not resp.ok:
            raise WechatSogouRequestsException('WechatSogouAPI search_gzh', resp)

        if 'antispider' in resp.url:
            self.__deblocking_search(url, resp, req, deblocking_callback, identify_image_callback)
            resp = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie())  # req=req

        return WechatSogouStructuring.get_gzh_by_search(resp.text)

    def search_article(self, keyword, page=1, timesn=0, article_type=WechatSogouRequest.TYPE_ALL, ft=None, et=None,
                       deblocking_callback=None, identify_image_callback=None):
        """搜索 文章

        对于出现验证码的情况，可以由使用者自己提供：
            1、函数 deblocking_callback ，这个函数 handle 出现验证码到解决的整个流程
            2、也可以 只提供函数 identify_image_callback，这个函数输入验证码二进制数据，输出验证码文字，剩下的由 wechatsogou 包来解决
        注意：
            函数 deblocking_callback 和 identify_image_callback 只需要提供一个，如果都提供了，那么 identify_image_callback 不起作用

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1
        timesn : {0, 1, 2, 3, 4, 5}
            时间 0 没有限制 / 1一天 / 2一周 / 3一月 / 4一年 / 5自定
            the default is 0
        article_type : {'image', 'video', 'rich', 'all'}
            含有内容的类型 TYPE_IMAGE 有图 / TYPE_VIDEO 有视频 / TYPE_RICH 有图和视频 / TYPE_ALL 啥都有
        ft, et : datetime.date or None
            当 tsn 是 5 时，ft 代表开始时间，如： 2017-07-01
            当 tsn 是 5 时，et 代表结束时间，如： 2017-07-15
        deblocking_callback : callable
            处理出现验证码页面的函数，参见 deblocking_callback_example
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        list[dict]
            {
                'article': {
                    'title': '',  # 文章标题
                    'url': '',  # 文章链接
                    'imgs': '',  # 文章图片list
                    'abstract': '',  # 文章摘要
                    'time': ''  # 文章推送时间
                },
                'gzh': {
                    'profile_url': '',  # 公众号最近10条群发页链接
                    'headimage': '',  # 头像
                    'wechat_name': '',  # 名称
                    'isv': '',  # 是否加v
                }
            }

        Raises
        ------
        WechatSogouRequestsException
            requests error
        """
        req = requests.session()

        url = WechatSogouRequest.gen_search_article_url(keyword, page, timesn=timesn, article_type=article_type, ft=ft,
                                                        et=et)
        url_referer = WechatSogouRequest.gen_search_article_url(keyword)

        resp = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie(referer=url_referer))

        if not resp.ok:
            raise WechatSogouRequestsException('WechatSogouAPI search_article', resp)

        if 'antispider' in resp.url:
            self.__deblocking_search(url, resp, req, deblocking_callback, identify_image_callback)
            resp = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie(referer=url_referer))  # req=req

        return WechatSogouStructuring.get_article_by_search(resp.text)

    def get_gzh_artilce_by_history(self, keyword=None, url=None, deblocking_callback=None,
                                   identify_image_callback=None):
        """从 公众号的最近10条群发页面 提取公众号信息 和 文章列表信息

        对于出现验证码的情况，可以由使用者自己提供：
            1、函数 deblocking_callback ，这个函数 handle 出现验证码到解决的整个流程
            2、也可以 只提供函数 identify_image_callback，这个函数输入验证码二进制数据，输出验证码文字，剩下的由 wechatsogou 包来解决
        注意：
            函数 deblocking_callback 和 identify_image_callback 只需要提供一个，如果都提供了，那么 identify_image_callback 不起作用

        Parameters
        ----------
        keyword : str or unicode
            公众号的id 或者name
        url : str or unicode
            群发页url，如果不提供url，就先去搜索一遍拿到url
        deblocking_callback : callable
            处理出现验证码页面的函数，参见 deblocking_callback_example
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        dict
            {
                'gzh_info': {
                    'wechat_name': '',  # 名称
                    'wechat_id': '',  # 微信id
                    'introduction': '',  # 描述
                    'authentication': '',  # 认证
                    'headimage': ''  # 头像
                },
                'article': [
                    {
                        'send_id': '',  # 群发id，注意不唯一，因为同一次群发多个消息，而群发id一致
                        'datetime': '',  # 群发datatime
                        'type': '',  # 消息类型，均是49，表示图文
                        'main': 0,  # 是否是一次群发的第一次消息
                        'title': '',  # 文章标题
                        'abstract': '',  # 摘要
                        'fileid': '',  #
                        'content_url': '',  # 文章链接
                        'source_url': '',  # 阅读原文的链接
                        'cover': '',  # 封面图
                        'author': '',  # 作者
                        'copyright_stat': '',  # 文章类型，例如：原创啊
                    },
                    ...
                ]
            }


        Raises
        ------
        WechatSogouRequestsException
            requests error
        """
        if url is None:
            gzh_list = self.get_gzh_info(keyword, deblocking_callback=deblocking_callback,
                                         identify_image_callback=identify_image_callback)
            if gzh_list:
                url = gzh_list['profile_url']
            else:
                raise Exception()  # todo use ws exception

        req = requests.session()

        resp = WechatSogouRequest.get(url, req=req)  # headers=self.__set_cookie()

        if not resp.ok:
            raise WechatSogouRequestsException('WechatSogouAPI get_gzh_artilce_by_history', resp)

        if '请输入验证码' in resp.text:
            self.__deblocking_history(url, resp, req, deblocking_callback, identify_image_callback)
            resp = WechatSogouRequest.get(url, req=req)  # req=req headers=self.__set_cookie()

        return WechatSogouStructuring.get_gzh_info_and_article_by_history(resp.text)

    def get_article_content(self):
        """获取 文章 原文 ， 避免临时链接失效

        :return:
        """

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
        pass  # todo
        # try:
        #     keyword = str(keyword) if type(keyword) != str else keyword
        # except Exception as e:
        #     logger.error('get_sugg keyword error', e)
        #     raise WechatSogouException('get_sugg keyword error')
        # url = 'http://w.sugg.sogou.com/sugg/ajaj_json.jsp?key=' + keyword + '&type=wxpub&pr=web'
        # text = self._get(url, 'get', host='w.sugg.sogou.com')
        # try:
        #     sugg = re.findall(u'\["' + keyword + '",(.*?),\["', text)[0]
        #     sugg = eval(sugg)
        #     return sugg
        # except Exception as e:
        #     logger.error('sugg refind error', e)
        #     raise WechatSogouException('sugg refind error')
