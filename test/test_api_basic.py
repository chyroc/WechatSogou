# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals, print_function)

import io
import os
import unittest
from nose.tools import assert_raises, assert_equal, assert_in

import httpretty
from hypothesis import given, strategies as st

from wechatsogou import refactor_basic
from wechatsogou.pkgs import unquote
from wechatsogou.refactor_basic import WechatSogouBasic


class TestBasicGenURL(unittest.TestCase):
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

    @given(st.integers(min_value=-50, max_value=50), st.dates(), st.dates())
    def test_gen_search_article_url_timesn(self, timesn, ft, et):
        if timesn in [1, 2, 3, 4]:
            url = WechatSogouBasic._gen_search_article_url('高考', timesn=timesn)
            assert_in('tsn={}&ft=&et='.format(timesn), url)

            url = WechatSogouBasic._gen_search_article_url('高考', timesn=timesn, ft=str(ft))
            assert_in('tsn={}&ft=&et='.format(timesn), url)
        elif timesn == 5:
            if ft <= et:
                url = WechatSogouBasic._gen_search_article_url('高考', timesn=timesn, ft=ft, et=et)
                assert_in('tsn=5&ft={}&et={}'.format(ft, et), url)
            else:
                with assert_raises(AssertionError):
                    WechatSogouBasic._gen_search_article_url('高考', timesn=timesn)
                    WechatSogouBasic._gen_search_article_url('高考', timesn=timesn, ft=ft, et=et)
        else:
            with assert_raises(AssertionError):
                WechatSogouBasic._gen_search_article_url('高考', timesn=timesn)

    def test_gen_search_article_url_article_type(self):
        url = WechatSogouBasic._gen_search_article_url('高考', article_type=refactor_basic.TYPE_ALL)
        assert_equal('interation=', url[-11:])

        url = WechatSogouBasic._gen_search_article_url('高考', article_type=refactor_basic.TYPE_IMAGE)
        assert_in('interation=458754', url)

        url = WechatSogouBasic._gen_search_article_url('高考', article_type=refactor_basic.TYPE_VIDEO)
        assert_in('interation=458756', url)

        url = WechatSogouBasic._gen_search_article_url('高考', article_type=refactor_basic.TYPE_RICH)
        assert_in('interation=458754%2C458756', url)


class TestBasicSearchArticle(unittest.TestCase):
    def setUp(self):
        self.ws = WechatSogouBasic()

    @httpretty.activate
    def test_search_article(self):
        file = '{}/{}'.format(os.getcwd(), 'test/file/search-gaokao-article.html')
        with io.open(file, encoding='utf-8') as f:
            search_gaokao_article = f.read()
            httpretty.register_uri(httpretty.GET, WechatSogouBasic._gen_search_article_url('高考'),
                                   body=search_gaokao_article)

        text = self.ws._search_article('高考')
        assert_equal(text, search_gaokao_article)


if __name__ == '__main__':
    unittest.main()
