# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import unittest
from nose.tools import assert_raises, assert_equal, assert_in

from hypothesis import given, strategies as st

from wechatsogou.request import WechatSogouRequest
from test import gaokao_keyword


class TestBasicGenSearchGzhURL(unittest.TestCase):
    def test_gen_search_article_url_keyword(self):
        url = WechatSogouRequest.gen_search_gzh_url(gaokao_keyword)
        assert_equal('http://weixin.sogou.com/weixin?type=1&page=1&ie=utf8&query=%E9%AB%98%E8%80%83', url)

    @given(st.integers(min_value=-20000, max_value=20000))
    def test_gen_search_gzh_url_page(self, page):
        if page > 0:
            url = WechatSogouRequest.gen_search_gzh_url(gaokao_keyword, page)
            assert_in('page={}'.format(page), url)
        else:
            with assert_raises(AssertionError):
                WechatSogouRequest.gen_search_gzh_url(gaokao_keyword, page)
