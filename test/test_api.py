# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import io
import os
import unittest
from nose.tools import assert_equal

import httpretty

from wechatsogou.request import WechatSogouRequest
from wechatsogou.api import WechatSogouAPI
from test import fake_data_path, gaokao_keyword

ws_api = WechatSogouAPI()


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

    @unittest.skip
    def test_search_gzh_error(self):
        pass  # todo


if __name__ == '__main__':
    unittest.main()
