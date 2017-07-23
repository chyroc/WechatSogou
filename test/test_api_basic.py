# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import io
import os
import unittest
from nose.tools import assert_raises, assert_equal, assert_in, assert_not_equal

import httpretty
from hypothesis import given, strategies as st

from wechatsogou.refactor_basic import WechatSogouBasic

gaokao_keyword = '高考'
ws = WechatSogouBasic()


class TestBasicGenSearchArticleURL(unittest.TestCase):
    def test_gen_search_article_url_keyword(self):
        url = WechatSogouBasic._gen_search_article_url(gaokao_keyword)
        assert_equal('http://weixin.sogou.com/weixin?type=2&page=1&ie=utf8&query=%E9%AB%98%E8%80%83&interation=', url)

    @given(st.integers(min_value=-20000, max_value=20000))
    def test_gen_search_article_url_page(self, page):
        if page > 0:
            url = WechatSogouBasic._gen_search_article_url(gaokao_keyword, page)
            assert_in('page={}'.format(page), url)
        else:
            with assert_raises(AssertionError):
                WechatSogouBasic._gen_search_article_url(gaokao_keyword, page)

    @given(st.integers(min_value=-50, max_value=50), st.dates(), st.dates())
    def test_gen_search_article_url_timesn(self, timesn, ft, et):
        if timesn in [1, 2, 3, 4]:
            url = WechatSogouBasic._gen_search_article_url(gaokao_keyword, timesn=timesn)
            assert_in('tsn={}&ft=&et='.format(timesn), url)

            url = WechatSogouBasic._gen_search_article_url(gaokao_keyword, timesn=timesn, ft=str(ft))
            assert_in('tsn={}&ft=&et='.format(timesn), url)
        elif timesn == 5:
            if ft <= et:
                url = WechatSogouBasic._gen_search_article_url(gaokao_keyword, timesn=timesn, ft=ft, et=et)
                assert_in('tsn=5&ft={}&et={}'.format(ft, et), url)
            else:
                with assert_raises(AssertionError):
                    WechatSogouBasic._gen_search_article_url(gaokao_keyword, timesn=timesn)
                    WechatSogouBasic._gen_search_article_url(gaokao_keyword, timesn=timesn, ft=ft, et=et)
        else:
            with assert_raises(AssertionError):
                WechatSogouBasic._gen_search_article_url(gaokao_keyword, timesn=timesn)

    def test_gen_search_article_url_article_type(self):
        url = WechatSogouBasic._gen_search_article_url(gaokao_keyword, article_type=WechatSogouBasic.TYPE_ALL)
        assert_equal('interation=', url[-11:])

        url = WechatSogouBasic._gen_search_article_url(gaokao_keyword, article_type=WechatSogouBasic.TYPE_IMAGE)
        assert_in('interation=458754', url)

        url = WechatSogouBasic._gen_search_article_url(gaokao_keyword, article_type=WechatSogouBasic.TYPE_VIDEO)
        assert_in('interation=458756', url)

        url = WechatSogouBasic._gen_search_article_url(gaokao_keyword, article_type=WechatSogouBasic.TYPE_RICH)
        assert_in('interation=458754%2C458756', url)


class TestBasicGenSearchGzhURL(unittest.TestCase):
    def test_gen_search_article_url_keyword(self):
        url = WechatSogouBasic._gen_search_gzh_url(gaokao_keyword)
        assert_equal('http://weixin.sogou.com/weixin?type=1&page=1&ie=utf8&query=%E9%AB%98%E8%80%83', url)

    @given(st.integers(min_value=-20000, max_value=20000))
    def test_gen_search_gzh_url_page(self, page):
        if page > 0:
            url = WechatSogouBasic._gen_search_gzh_url(gaokao_keyword, page)
            assert_in('page={}'.format(page), url)
        else:
            with assert_raises(AssertionError):
                WechatSogouBasic._gen_search_gzh_url(gaokao_keyword, page)


class TestBasicSearchArticle(unittest.TestCase):
    @httpretty.activate
    def test_search_article_keyword(self):
        url = WechatSogouBasic._gen_search_article_url(gaokao_keyword)
        file_name = '{}/{}'.format(os.getcwd(), 'test/file/search-gaokao-article.html')
        with io.open(file_name, encoding='utf-8') as f:
            search_gaokao_article = f.read()
            httpretty.register_uri(httpretty.GET, url, body=search_gaokao_article)

        r = WechatSogouBasic._search_article(gaokao_keyword)
        assert_equal(search_gaokao_article, r.text)
        assert_equal(url, r.url)
        assert_not_equal(WechatSogouBasic._gen_search_article_url(gaokao_keyword, 2), r.url)
        assert_not_equal(WechatSogouBasic._search_gzh(gaokao_keyword), r.url)


class TestBasicSearchGzh(unittest.TestCase):
    @httpretty.activate
    def test_search_gzh_keyword(self):
        url = WechatSogouBasic._gen_search_gzh_url(gaokao_keyword)
        file_name = '{}/{}'.format(os.getcwd(), 'test/file/search-gaokao-gzh.html')
        with io.open(file_name, encoding='utf-8') as f:
            search_gaokao_gzh = f.read()
            httpretty.register_uri(httpretty.GET, url, body=search_gaokao_gzh)

        r = WechatSogouBasic._search_gzh(gaokao_keyword)
        assert_equal(search_gaokao_gzh, r.text)
        assert_equal(url, r.url)
        assert_not_equal(WechatSogouBasic._search_gzh(gaokao_keyword, 2), r.url)
        assert_not_equal(WechatSogouBasic._search_article(gaokao_keyword), r.url)


if __name__ == '__main__':
    unittest.main()
