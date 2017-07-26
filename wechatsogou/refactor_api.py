# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import time

import requests

from wechatsogou.exceptions import WechatSogouRequestsExceptionRefactor, WechatSogouVcodeOcrException
from wechatsogou.refactor_request import WechatSogouRequest
from wechatsogou.refactor_structuring import WechatSogouStructuring
from wechatsogou.identify_image import ws_cache, identify_image_callback_example, deblocking_callback_example


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
            raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI get img', resp)

        if callable(deblocking_callback):
            r_deblocking = deblocking_callback(req, resp, r_img.content)
        else:
            if callable(identify_image_callback):
                r_deblocking = deblocking_callback_example(url, req, resp, r_img.content,
                                                           identify_image_callback=identify_image_callback)
            else:
                r_deblocking = deblocking_callback_example(url, req, resp, r_img.content,
                                                           identify_image_callback=identify_image_callback_example)

        if r_deblocking['code'] != 0:
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {code}, msg: {msg}'.format(**r_deblocking))
        else:
            self.__set_cache(req.cookies.get('SUID'), r_deblocking['id'])

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
                'url': '',
                'img': '',
                'name': '',
                'wechat_id': '',
                'post_perm': '',
                'qrcode': '',
                'introduction': '',
                'authentication': ''
            }

        Raises
        ------
        WechatSogouRequestsException
            requests error
        """
        req = requests.session()

        url = WechatSogouRequest._gen_search_gzh_url(keyword, page)
        resp = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie())

        if not resp.ok:
            raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI search_gzh', resp)

        if 'antispider' in resp.url:
            self.__deblocking_search(url, resp, req, deblocking_callback, identify_image_callback)

        headers = self.__set_cookie()
        r = WechatSogouRequest.get(url, req=req, headers=headers)  # req=req

        return WechatSogouStructuring.get_gzh_by_search(r.text)

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
                'url': '',
                'img': '',
                'name': '',
                'wechat_id': '',
                'post_perm': '',
                'qrcode': '',
                'introduction': '',
                'authentication': ''
            }

        Raises
        ------
        WechatSogouRequestsException
            requests error
        """
        req = requests.session()

        url = WechatSogouRequest._gen_search_article_url(keyword, page, timesn=timesn, article_type=article_type, ft=ft,
                                                         et=et)
        url_referer = WechatSogouRequest._gen_search_article_url(keyword)

        resp = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie(referer=url_referer))

        if not resp.ok:
            raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI search_article', resp)

        if 'antispider' in resp.url:
            self.__deblocking_search(url, resp, req, deblocking_callback, identify_image_callback)

        r = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie(referer=url_referer))  # req=req

        return WechatSogouStructuring.get_article_by_search(r.text)
