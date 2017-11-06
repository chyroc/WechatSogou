# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import re
import json
import time

import requests

from wechatsogou.five import quote
from wechatsogou.const import WechatSogouConst
from wechatsogou.request import WechatSogouRequest
from wechatsogou.structuring import WechatSogouStructuring
from wechatsogou.exceptions import WechatSogouRequestsException, WechatSogouVcodeOcrException
from wechatsogou.identify_image import (
    ws_cache,
    identify_image_callback_by_hand,
    unlock_sogou_callback_example,
    unlock_weixin_callback_example)


class WechatSogouAPI(object):
    def __init__(self, captcha_break_time=1, **kwargs):
        """初始化参数

        Parameters
        ----------
        captcha_break_time : int
            验证码输入错误重试次数
        proxies : dict
            代理
        timeout : float
            超时时间
        """
        assert isinstance(captcha_break_time, int) and 0 < captcha_break_time < 20

        self.captcha_break_times = captcha_break_time
        self.requests_kwargs = kwargs

    def __set_cookie(self, suv=None, snuid=None, referer=None):
        suv = ws_cache.get('suv') if suv is None else suv
        snuid = ws_cache.get('snuid') if snuid is None else snuid

        _headers = {'Cookie': 'SUV={};SNUID={};'.format(suv, snuid)}
        if referer is not None:
            _headers['Referer'] = referer
        return _headers

    def __set_cache(self, suv, snuid):
        ws_cache.set('suv', suv)
        ws_cache.set('snuid', snuid)

    def __get(self, url, session, headers):
        resp = session.get(url, headers=headers, **self.requests_kwargs)

        if not resp.ok:
            raise WechatSogouRequestsException('WechatSogouAPI get error', resp)

        return resp

    def __unlock_sogou(self, url, resp, session, unlock_callback=None, identify_image_callback=None):
        if unlock_callback is None:
            unlock_callback = unlock_sogou_callback_example

        millis = int(round(time.time() * 1000))
        r_captcha = session.get('http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(millis))
        if not r_captcha.ok:
            raise WechatSogouRequestsException('WechatSogouAPI get img', resp)

        r_unlock = unlock_callback(url, session, resp, r_captcha.content, identify_image_callback)

        if r_unlock['code'] != 0:
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {code}, msg: {msg}'.format(code=r_unlock.get('code'),
                                                                                  msg=r_unlock.get('msg')))
        else:
            self.__set_cache(session.cookies.get('SUID'), r_unlock['id'])

    def __unlock_wechat(self, url, resp, session, unlock_callback=None, identify_image_callback=None):
        if unlock_callback is None:
            unlock_callback = unlock_weixin_callback_example

        r_captcha = session.get('https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(time.time() * 1000))
        if not r_captcha.ok:
            raise WechatSogouRequestsException('WechatSogouAPI unlock_history get img', resp)

        r_unlock = unlock_callback(url, session, resp, r_captcha.content, identify_image_callback)

        if r_unlock['ret'] != 0:
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {ret}, msg: {errmsg}, cookie_count: {cookie_count}'.format(
                    ret=r_unlock.get('ret'), errmsg=r_unlock.get('errmsg'), cookie_count=r_unlock.get('cookie_count')))

    def __get_by_unlock(self, url, referer=None, unlock_platform=None, unlock_callback=None,
                        identify_image_callback=None):
        assert unlock_platform is None or callable(unlock_platform)

        if identify_image_callback is None:
            identify_image_callback = identify_image_callback_by_hand
        assert unlock_callback is None or callable(unlock_callback)
        assert callable(identify_image_callback)

        session = requests.session()
        resp = self.__get(url, session, headers=self.__set_cookie(referer=referer))

        if 'antispider' in resp.url or '请输入验证码' in resp.text:
            for i in range(self.captcha_break_times):
                try:
                    unlock_platform(url, resp, session, unlock_callback, identify_image_callback)
                    break
                except WechatSogouVcodeOcrException as e:
                    if i == self.captcha_break_times - 1:
                        raise WechatSogouVcodeOcrException(e)

            resp = self.__get(url, session, headers=self.__set_cookie(referer=referer))

        return resp

    def get_gzh_info(self, wecgat_id_or_name, unlock_callback=None, identify_image_callback=None):
        """获取公众号微信号 wechatid 的信息

        因为wechatid唯一确定，所以第一个就是要搜索的公众号

        Parameters
        ----------
        wecgat_id_or_name : str or unicode
            wechat_id or wechat_name
        unlock_callback : callable
            处理出现验证码页面的函数，参见 unlock_callback_example
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        dict or None
            {
                'open_id': '', # 微信号唯一ID
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
        info = self.search_gzh(wecgat_id_or_name, 1, unlock_callback, identify_image_callback)
        return info[0] if info else None

    def search_gzh(self, keyword, page=1, unlock_callback=None, identify_image_callback=None):
        """搜索 公众号

        对于出现验证码的情况，可以由使用者自己提供：
            1、函数 unlock_callback ，这个函数 handle 出现验证码到解决的整个流程
            2、也可以 只提供函数 identify_image_callback，这个函数输入验证码二进制数据，输出验证码文字，剩下的由 wechatsogou 包来解决
        注意：
            函数 unlock_callback 和 identify_image_callback 只需要提供一个，如果都提供了，那么 identify_image_callback 不起作用

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1
        unlock_callback : callable
            处理出现验证码页面的函数，参见 unlock_callback_example
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        list[dict]
            {
                'open_id': '', # 微信号唯一ID
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
        url = WechatSogouRequest.gen_search_gzh_url(keyword, page)
        resp = self.__get_by_unlock(url,
                                    unlock_platform=self.__unlock_sogou,
                                    unlock_callback=unlock_callback,
                                    identify_image_callback=identify_image_callback)

        return WechatSogouStructuring.get_gzh_by_search(resp.text)

    def search_article(self, keyword, page=1, timesn=WechatSogouConst.search_article_time.anytime,
                       article_type=WechatSogouConst.search_article_type.all, ft=None, et=None,
                       unlock_callback=None,
                       identify_image_callback=None):
        """搜索 文章

        对于出现验证码的情况，可以由使用者自己提供：
            1、函数 unlock_callback ，这个函数 handle 出现验证码到解决的整个流程
            2、也可以 只提供函数 identify_image_callback，这个函数输入验证码二进制数据，输出验证码文字，剩下的由 wechatsogou 包来解决
        注意：
            函数 unlock_callback 和 identify_image_callback 只需要提供一个，如果都提供了，那么 identify_image_callback 不起作用

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1
        timesn : WechatSogouConst.search_article_time
            时间 anytime 没有限制 / day 一天 / week 一周 / month 一月 / year 一年 / specific 自定
            the default is anytime
        article_type : WechatSogouConst.search_article_type
            含有内容的类型 image 有图 / video 有视频 / rich 有图和视频 / all 啥都有
        ft, et : datetime.date or None
            当 tsn 是 specific 时，ft 代表开始时间，如： 2017-07-01
            当 tsn 是 specific 时，et 代表结束时间，如： 2017-07-15
        unlock_callback : callable
            处理出现验证码页面的函数，参见 unlock_callback_example
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
        url = WechatSogouRequest.gen_search_article_url(keyword, page, timesn, article_type, ft, et)
        resp = self.__get_by_unlock(url, WechatSogouRequest.gen_search_article_url(keyword),
                                    unlock_platform=self.__unlock_sogou,
                                    unlock_callback=unlock_callback,
                                    identify_image_callback=identify_image_callback)

        return WechatSogouStructuring.get_article_by_search(resp.text)

    def get_gzh_article_by_history(self, keyword=None, url=None,
                                   unlock_callback_sogou=None,
                                   identify_image_callback_sogou=None,
                                   unlock_callback_weixin=None,
                                   identify_image_callback_weixin=None):
        """从 公众号的最近10条群发页面 提取公众号信息 和 文章列表信息

        对于出现验证码的情况，可以由使用者自己提供：
            1、函数 unlock_callback ，这个函数 handle 出现验证码到解决的整个流程
            2、也可以 只提供函数 identify_image_callback，这个函数输入验证码二进制数据，输出验证码文字，剩下的由 wechatsogou 包来解决
        注意：
            函数 unlock_callback 和 identify_image_callback 只需要提供一个，如果都提供了，那么 identify_image_callback 不起作用

        Parameters
        ----------
        keyword : str or unicode
            公众号的id 或者name
        url : str or unicode
            群发页url，如果不提供url，就先去搜索一遍拿到url
        unlock_callback_sogou : callable
            处理出现 搜索 的时候出现验证码的函数，参见 unlock_callback_example
        identify_image_callback_sogou : callable
            处理 搜索 的时候处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example
        unlock_callback_weixin : callable
            处理出现 历史页 的时候出现验证码的函数，参见 unlock_callback_example
        identify_image_callback_weixin : callable
            处理 历史页 的时候处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        dict
            {
                'gzh': {
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
            gzh_list = self.get_gzh_info(keyword, unlock_callback_sogou, identify_image_callback_sogou)
            if 'profile_url' not in gzh_list:
                raise Exception()  # todo use ws exception
            url = gzh_list['profile_url']

        resp = self.__get_by_unlock(url, WechatSogouRequest.gen_search_article_url(keyword),
                                    unlock_platform=self.__unlock_wechat,
                                    unlock_callback=unlock_callback_weixin,
                                    identify_image_callback=identify_image_callback_weixin)

        return WechatSogouStructuring.get_gzh_info_and_article_by_history(resp.text)

    def get_gzh_article_by_hot(self, hot_index, page=1, unlock_callback=None, identify_image_callback=None):
        """获取 首页热门文章

        Parameters
        ----------
        hot_index : WechatSogouConst.hot_index
            首页热门文章的分类（常量）：WechatSogouConst.hot_index.xxx
        page : int
            页数

        Returns
        -------
        list[dict]
            {
                'gzh': {
                    'headimage': str,  # 公众号头像
                    'wechat_name': str,  # 公众号名称
                },
                'article': {
                    'url': str,  # 文章临时链接
                    'title': str,  # 文章标题
                    'abstract': str,  # 文章摘要
                    'time': int,  # 推送时间，10位时间戳
                    'open_id': str,  # open id
                    'main_img': str  # 封面图片
                }
            }
        """

        assert hasattr(WechatSogouConst.hot_index, hot_index)
        assert isinstance(page, int) and page > 0

        url = WechatSogouRequest.gen_hot_url(hot_index, page)
        resp = self.__get_by_unlock(url,
                                    unlock_platform=self.__unlock_sogou,
                                    unlock_callback=unlock_callback,
                                    identify_image_callback=identify_image_callback)

        resp.encoding = 'utf-8'
        return WechatSogouStructuring.get_gzh_article_by_hot(resp.text)

    def get_article_content(self):
        """获取文章原文，避免临时链接失效

        :return:
        """
        pass  # TODO 获取文章原文，避免临时链接失效

    def get_sugg(self, keyword):
        """获取微信搜狗搜索关键词联想

        Parameters
        ----------
        keyword : str or unicode
            关键词

        Returns
        -------
        list[str]
            联想关键词列表

        Raises
        ------
        WechatSogouRequestsException
        """
        url = 'http://w.sugg.sogou.com/sugg/ajaj_json.jsp?key={}&type=wxpub&pr=web'.format(
            quote(keyword.encode('utf-8')))
        r = requests.get(url)
        if not r.ok:
            raise WechatSogouRequestsException('get_sugg', r)

        sugg = re.findall(u'\["' + keyword + '",(.*?),\["', r.text)[0]
        return json.loads(sugg)
