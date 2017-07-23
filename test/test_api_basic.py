# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import,
    unicode_literals,
    print_function
)

import io
import os
import unittest
from nose.tools import assert_raises, assert_equal, assert_in

import httpretty
from hypothesis import given, strategies as st

import wechatsogou.tools
from wechatsogou.tools import unquote
from wechatsogou.refactor_basic import WechatSogouBasic


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.ws = WechatSogouBasic()

    def test_gen_search_article_url_keyword(self):
        url = WechatSogouBasic._gen_search_article_url('高考')
        assert_equal('http://weixin.sogou.com/weixin?type=2&page=1&ie=utf8&query=%E9%AB%98%E8%80%83&interation=', url)

    @given(st.integers(min_value=-20000, max_value=20000))
    def test_gen_search_article_url_page(self, page):
        if page > 0:
            url = WechatSogouBasic._gen_search_article_url('高考', page)
            assert_in('page={}'.format(page), url)
        else:
            with assert_raises(AssertionError):
                WechatSogouBasic._gen_search_article_url('高考', page)

    @given(st.integers(min_value=-50, max_value=50))
    def test_gen_search_article_url_timesn(self, timesn):
        if timesn in [1, 2, 3, 4]:
            url = WechatSogouBasic._gen_search_article_url('高考', timesn=timesn)
        elif timesn == 5:
            pass
        else:
            with assert_raises(AssertionError):
                WechatSogouBasic._gen_search_article_url('高考', timesn=timesn)

        # assert_equal(url,
        #              'http://weixin.sogou.com/weixin?type=2&page=1&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=1&ft=&et=&interation=')
        # assert_equal(WechatSogouBasic._gen_search_article_url('高考', timesn=1, ft='2017-01-32', et='2017-12-32'),
        #              'http://weixin.sogou.com/weixin?type=2&page=1&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=1&ft=&et=&interation=')
        # with assert_raises(AssertionError):
        #     WechatSogouBasic._gen_search_article_url('高考', timesn=5, ft='2017-01-32', et='2017-12-32')
        #     WechatSogouBasic._gen_search_article_url('高考', timesn=6, ft='2017-01-32', et='2017-12-32')
        #     WechatSogouBasic._gen_search_article_url('高考', timesn='', ft='2017-01-32', et='2017-12-32')

        # assert_equal(WechatSogouBasic._gen_search_url('高考', 2),
        #              'http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83')
        # with assert_raises(AssertionError):
        #     assert_equal(WechatSogouBasic._gen_search_url('高考', 3),
        #                  'http://weixin.sogou.com/weixin?type=3&ie=utf8&query=%E9%AB%98%E8%80%83')

        """
        @httpretty.activate
        def test_search_article(self):
            file = '{}/{}'.format(os.getcwd(), 'test/file/search-gaokao-article.html')
            with io.open(file, encoding='utf-8') as f:
                search_gaokao_article = f.read()
                httpretty.register_uri(httpretty.GET, WechatSogouBasic._gen_search_url('高考', 2), body=search_gaokao_article)
    
            text = self.ws._search('高考', 2)
            assert_equal(text, search_gaokao_article)
        """


if __name__ == '__main__':
    unittest.main()
