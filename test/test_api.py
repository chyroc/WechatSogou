# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import io
import os
import unittest

from nose.tools import assert_equal, assert_true, assert_in, assert_greater_equal
import httpretty

from wechatsogou.request import WechatSogouRequest
from wechatsogou.api import WechatSogouAPI
from test import fake_data_path, gaokao_keyword
from test.rk import identify_image_callback_ruokuai_search, identify_image_callback_ruokuai_history

ws_api = WechatSogouAPI(captcha_break_time=3)


class TestAPI(unittest.TestCase):
    @httpretty.activate
    def test_search_gzh(self):
        url = WechatSogouRequest.gen_search_gzh_url(gaokao_keyword)
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'search-gaokao-gzh.html')
        with io.open(file_name, encoding='utf-8') as f:
            search_gaokao_gzh_error = f.read()
            httpretty.register_uri(httpretty.GET, url, body=search_gaokao_gzh_error)

        gzh_list = ws_api.search_gzh(gaokao_keyword)
        assert_equal(10, len(gzh_list))
        assert_equal(['山东高考指南',
                      '高考家长圈',
                      '河南高考指南',
                      '高考360',
                      '云天高考',
                      '腾讯高考',
                      '高考快讯',
                      '专业中高考教育',
                      '晟嘉高考',
                      '新东方在线高考辅导'],
                     [i['wechat_name'] for i in gzh_list])

    # todo use chinese qq
    def test_search_gzh_real(self):
        gzh_list = ws_api.search_gzh(gaokao_keyword, identify_image_callback=identify_image_callback_ruokuai_search)
        assert_equal(10, len(gzh_list))
        assert_true(any(gaokao_keyword in i['wechat_name'] for i in gzh_list))

    def test_get_gzh_artilce_by_history_real(self):
        gzh_artilce = ws_api.get_gzh_artilce_by_history(gaokao_keyword,
                                                        identify_image_callback_search=identify_image_callback_ruokuai_search,
                                                        identify_image_callback_history=identify_image_callback_ruokuai_history)
        assert_in('gzh_info', gzh_artilce)
        assert_in('article', gzh_artilce)
        assert_in('wx.qlogo.cn', gzh_artilce['gzh_info']['headimage'])
        assert_greater_equal(len(gzh_artilce['article']), 1)

    def test_get_sugg(self):
        sugg_gaokao = ws_api.get_sugg(gaokao_keyword)
        assert_equal(10, len(sugg_gaokao))


if __name__ == '__main__':
    unittest.main()
