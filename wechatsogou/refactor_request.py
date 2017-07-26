# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import datetime
from collections import OrderedDict

import requests

from wechatsogou.pkgs import urlencode


class WechatSogouRequest(object):
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_RICH = 'rich'
    TYPE_ALL = 'all'

    @staticmethod
    def _gen_search_article_url(keyword, page=1, timesn=0, article_type=TYPE_ALL, wxid=None, usip=None, ft=None,
                                et=None):
        """拼接搜索 文章 URL

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
        wxid : None
            wxid usip 联合起来就是账号内搜索
        usip : None
            wxid usip 联合起来就是账号内搜索
        ft, et : datetime.date
            当 tsn 是 5 时，ft 代表开始时间，如： 2017-07-01
            当 tsn 是 5 时，et 代表结束时间，如： 2017-07-15

        Returns
        -------
        str
            search_article_url
        """

        assert isinstance(page, int) and page > 0
        assert timesn in [0, 1, 2, 3, 4, 5]

        if timesn == 5:
            assert isinstance(ft, datetime.date)
            assert isinstance(et, datetime.date)
            assert ft <= et
        else:
            ft = ''
            et = ''

        interation_image = 458754
        interation_video = 458756
        if article_type == 'rich':
            interation = '{},{}'.format(interation_image, interation_video)
        elif article_type == 'image':
            interation = interation_image
        elif article_type == 'video':
            interation = interation_video
        else:
            interation = ''

        qsDict = OrderedDict()
        qsDict['type'] = 2  # 2 是文章
        qsDict['page'] = page
        qsDict['ie'] = 'utf8'
        qsDict['query'] = keyword
        if timesn != 0:
            qsDict['tsn'] = timesn
            qsDict['ft'] = str(ft)
            qsDict['et'] = str(et)
        qsDict['interation'] = interation

        # TODO 账号内搜索
        # '账号内 http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=3&ft=&et=&interation=458754
        # &wxid=oIWsFt1tmWoG6vO6BcsS7St61bRE&usip=nanhangqinggong'
        # qs['wxid'] = wxid
        # qs['usip'] = usip

        return 'http://weixin.sogou.com/weixin?{}'.format(urlencode(qsDict))

    @staticmethod
    def _gen_search_gzh_url(keyword, page=1):
        """拼接搜索 公众号 URL

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1

        Returns
        -------
        str
            search_gzh_url
        """
        assert isinstance(page, int) and page > 0

        qs_dict = OrderedDict()
        qs_dict['type'] = 1  # 1 是公号
        qs_dict['page'] = page
        qs_dict['ie'] = 'utf8'
        qs_dict['query'] = keyword

        return 'http://weixin.sogou.com/weixin?{}'.format(urlencode(qs_dict))

    @staticmethod
    def get(url, req=None, **kwargs):
        """搜索 公众号 获取文本

        Parameters
        ----------
        url : str or unicode
            url
        req : requests.sessions.Session
            requests.Session()

        Returns
        -------
        requests.models.Response
            return of requests
        """
        if isinstance(req, requests.sessions.Session):
            r = req.get(url, **kwargs)
        else:
            r = requests.get(url, **kwargs)

        return r
