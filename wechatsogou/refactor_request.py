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
    def _gen_search_article_url(keyword, page=1, timesn=None, article_type=TYPE_ALL, wxid=None, usip=None, ft=None,
                                et=None):
        """ 拼接搜索 文章 URL

        :param keyword:      搜索文字
        :param page:         页数
        :param timesn:       时间 1一天 / 2一周 / 3一月 / 4一年 / 5自定
        :param ft:           当 tsn 是 5 时，本参数代表时间，如： 2017-07-01
        :param et:           当 tsn 是 5 时，本参数代表时间，如： 2017-07-15
        :param artilce_type: 含有内容的类型： TYPE_IMAGE 有图 / TYPE_VIDEO 有视频 / TYPE_RICH 有图和视频 / TYPE_ALL 啥都有
        :param wxid:
        :param usip:         wxid usip 联合起来就是账号内搜索
        :return:
        """

        assert isinstance(page, int) and page > 0
        assert timesn in [1, 2, 3, 4, 5, None]

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
        if timesn is not None:
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
        """ 拼接搜索 公众号 URL

        :param keyword: 搜索文字
        :param page:    页数
        :return:
        """

        assert isinstance(page, int) and page > 0

        qsDict = OrderedDict()
        qsDict['type'] = 1  # 1 是公号
        qsDict['page'] = page
        qsDict['ie'] = 'utf8'
        qsDict['query'] = keyword

        return 'http://weixin.sogou.com/weixin?{}'.format(urlencode(qsDict))

    @staticmethod
    def _search_article(keyword, page=1, timesn=None, article_type=None, wxid=None, usip=None, ft=None, et=None):
        """搜索 文章 获取文本

        :param keyword: 关键词
        :param page: 页数
        :param timesn: 时间 1一天 / 2一周 / 3一月 / 4一年 / 5自定
        :param article_type: 含有内容的类型： TYPE_IMAGE 有图 / TYPE_VIDEO 有视频 / TYPE_RICH 有图和视频 / TYPE_ALL 啥都有
        :param wxid:
        :param usip: wxid usip 联合起来就是账号内搜索
        :param ft: 当 tsn 是 5 时，本参数代表时间，如： 2017-07-01
        :param et: 当 tsn 是 5 时，本参数代表时间，如： 2017-07-15
        :return:
        """
        url = WechatSogouRequest._gen_search_article_url(keyword, page, timesn, article_type, wxid, usip, ft, et)
        r = requests.get(url)
        if not r.ok:
            # todo 错误处理
            return None
        return r

    @staticmethod
    def _search_gzh(keyword, page=1):
        """搜索 公众号 获取文本

        :param keyword: 公众号关键词 / 微信号
        :param page:    页数 1-n
        :return:
        """
        url = WechatSogouRequest._gen_search_gzh_url(keyword, page)
        r = requests.get(url)
        if not r.ok:
            # todo 错误处理
            return None
        return r
