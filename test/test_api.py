# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import os
import unittest

from nose.tools import assert_equal, assert_true, assert_in, assert_greater_equal

from wechatsogou.const import WechatSogouConst
from wechatsogou.api import WechatSogouAPI
from wechatsogou.identify_image import identify_image_callback_by_hand
from test import gaokao_keyword
from test.rk import identify_image_callback_ruokuai_sogou, identify_image_callback_ruokuai_weixin

ws_api = WechatSogouAPI(captcha_break_time=3)


class TestAPIReal(unittest.TestCase):
    # todo use chinese
    def setUp(self):
        self.identify_image_callback_sogou = identify_image_callback_ruokuai_sogou if os.environ.get(
            'WechatSogouCI') else identify_image_callback_by_hand
        self.identify_image_callback_ruokuai_weixin = identify_image_callback_ruokuai_weixin if os.environ.get(
            'WechatSogouCI') else identify_image_callback_by_hand

    def test_search_gzh_real(self):
        gzh_list = ws_api.search_gzh(gaokao_keyword, identify_image_callback=self.identify_image_callback_sogou)
        assert_equal(10, len(gzh_list))
        assert_true(any(gaokao_keyword in i['wechat_name'] for i in gzh_list))
        assert_true(any(i['open_id'] != '' for i in gzh_list))

    def test_get_gzh_article_by_history_real(self):
        gzh_article = ws_api.get_gzh_article_by_history(gaokao_keyword,
                                                        identify_image_callback_sogou=self.identify_image_callback_sogou,
                                                        identify_image_callback_weixin=self.identify_image_callback_ruokuai_weixin)
        assert_in('gzh', gzh_article)
        assert_in('article', gzh_article)
        assert_in('wx.qlogo.cn', gzh_article['gzh']['headimage'])
        assert_greater_equal(len(gzh_article['article']), 1)

    def test_get_gzh_article_by_hot_real(self):
        gzh_articles = ws_api.get_gzh_article_by_hot(WechatSogouConst.hot_index.recommendation,
                                                     identify_image_callback=self.identify_image_callback_sogou)
        for gzh_article in gzh_articles:
            assert_in('gzh', gzh_article)
            assert_in('article', gzh_article)
            assert_in('http://mp.weixin.qq.com/s?src=', gzh_article['article']['url'])
        assert_greater_equal(len(gzh_articles), 10)

    def test_get_sugg(self):
        sugg_gaokao = ws_api.get_sugg(gaokao_keyword)
        assert_equal(10, len(sugg_gaokao))


if __name__ == '__main__':
    unittest.main()
