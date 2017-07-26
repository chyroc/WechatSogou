# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import io
import os
import unittest
from nose.tools import assert_equal, assert_not_equal

import httpretty

from wechatsogou.refactor_request import WechatSogouRequest
from wechatsogou.refactor_api import WechatSogouAPI
from test.test_main import fake_data_path, gaokao_keyword

ws_api = WechatSogouAPI()


class TestAPI(unittest.TestCase):
    @httpretty.activate
    def test_search_gzh(self):
        url = WechatSogouRequest._gen_search_gzh_url(gaokao_keyword)
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
                     [i['name'] for i in gzh_list])

    @httpretty.activate
    def test_search_gzh_error(self):
        url = WechatSogouRequest._gen_search_gzh_url(gaokao_keyword)
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'search-gaokao-gzh-error.html')
        with io.open(file_name, encoding='utf-8') as f:
            search_gaokao_gzh_error = f.read()
            httpretty.register_uri(httpretty.GET, url, body=search_gaokao_gzh_error)

        gzh_list = ws_api.search_gzh(gaokao_keyword)
        print(gzh_list)


if __name__ == '__main__':
    unittest.main()
