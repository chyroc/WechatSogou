# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import datetime
from collections import OrderedDict

import requests

from wechatsogou.pkgs import urlencode
from wechatsogou.const import WechatSogouConst


class WechatSogouRequest(object):
    @staticmethod
    def gen_search_article_url(keyword, page=1, timesn=0, article_type=WechatSogouConst.search_article_type.all,
                               ft=None, et=None):
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
        article_type : WechatSogouConst.search_article_type
            含有内容的类型 image 有图 / video 有视频 / rich 有图和视频 / all 啥都有
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
    def gen_search_gzh_url(keyword, page=1):
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
    def gen_hot_url(hot_index, page=1):
        """拼接 首页热门文章 URL

        Parameters
        ----------
        hot_index : str or unicode
            首页热门文章的分类（常量）：WechatSogouConst.hot_index.xxx
        page : int
            页数

        Returns
        -------
        str
            热门文章分类的url
        """

        assert hasattr(WechatSogouConst.hot_index, hot_index)
        assert isinstance(page, int) and page > 0
        hot_index = getattr(WechatSogouConst.hot_index, hot_index)

        index_urls = {
            WechatSogouConst.hot_index.hot: 0,  # 热门
            WechatSogouConst.hot_index.recommendation: 1,  # 推荐
            WechatSogouConst.hot_index.duanzi: 2,  # 段子手
            WechatSogouConst.hot_index.health: 3,  # 养生
            WechatSogouConst.hot_index.sifanghua: 4,  # 私房话
            WechatSogouConst.hot_index.gossip: 5,  # 八卦
            WechatSogouConst.hot_index.life: 6,  # 生活
            WechatSogouConst.hot_index.finance: 7,  # 财经
            WechatSogouConst.hot_index.car: 8,  # 汽车
            WechatSogouConst.hot_index.technology: 9,  # 科技
            WechatSogouConst.hot_index.fashion: 10,  # 时尚
            WechatSogouConst.hot_index.mummy: 11,  # 辣妈
            WechatSogouConst.hot_index.dianzan: 12,  # 点赞
            WechatSogouConst.hot_index.travel: 13,  # 旅行
            WechatSogouConst.hot_index.job: 14,  # 职场
            WechatSogouConst.hot_index.food: 15,  # 美食
            WechatSogouConst.hot_index.history: 16,  # 历史
            WechatSogouConst.hot_index.study: 17,  # 学霸
            WechatSogouConst.hot_index.constellation: 18,  # 星座
            WechatSogouConst.hot_index.sport: 19,  # 体育
        }
        return 'http://weixin.sogou.com/wapindex/wap/0612/wap_{}/{}.html'.format(index_urls[hot_index], page - 1)

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
