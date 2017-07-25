# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import unittest
from nose.tools import assert_raises, assert_equal, assert_in, assert_not_in

from hypothesis import given, strategies as st

from wechatsogou.refactor_request import WechatSogouRequest

gaokao_keyword = '高考'
ws = WechatSogouRequest()


class TestBasicGenSearchArticleURL(unittest.TestCase):
    def test_gen_search_article_url_keyword(self):
        url = WechatSogouRequest._gen_search_article_url(gaokao_keyword)
        assert_equal('http://weixin.sogou.com/weixin?type=2&page=1&ie=utf8&query=%E9%AB%98%E8%80%83&interation=', url)

    @given(st.integers(min_value=-20000, max_value=20000))
    def test_gen_search_article_url_page(self, page):
        if page > 0:
            url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, page)
            assert_in('page={}'.format(page), url)
        else:
            with assert_raises(AssertionError):
                WechatSogouRequest._gen_search_article_url(gaokao_keyword, page)

    @given(st.integers(min_value=-50, max_value=50), st.dates(), st.dates())
    def test_gen_search_article_url_timesn(self, timesn, ft, et):
        if timesn == 0:
            url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, timesn=timesn)
            assert_in('type=2&page=1&ie=utf8&query=', url)
            assert_not_in('ft=&et=', url)

            url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, timesn=timesn, ft=ft)
            assert_in('type=2&page=1&ie=utf8&query=', url)
            assert_not_in('ft=&et=', url)
        elif timesn in [1, 2, 3, 4]:
            url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, timesn=timesn)
            assert_in('tsn={}&ft=&et='.format(timesn), url)

            url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, timesn=timesn, ft=ft)
            assert_in('tsn={}&ft=&et='.format(timesn), url)
        elif timesn == 5:
            if ft <= et:
                url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, timesn=timesn, ft=ft, et=et)
                assert_in('tsn=5&ft={}&et={}'.format(ft, et), url)
            else:
                with assert_raises(AssertionError):
                    WechatSogouRequest._gen_search_article_url(gaokao_keyword, timesn=timesn)
                    WechatSogouRequest._gen_search_article_url(gaokao_keyword, timesn=timesn, ft=ft, et=et)
        else:
            with assert_raises(AssertionError):
                WechatSogouRequest._gen_search_article_url(gaokao_keyword, timesn=timesn)

    def test_gen_search_article_url_article_type(self):
        url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, article_type=WechatSogouRequest.TYPE_ALL)
        assert_equal('interation=', url[-11:])

        url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, article_type=WechatSogouRequest.TYPE_IMAGE)
        assert_in('interation=458754', url)

        url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, article_type=WechatSogouRequest.TYPE_VIDEO)
        assert_in('interation=458756', url)

        url = WechatSogouRequest._gen_search_article_url(gaokao_keyword, article_type=WechatSogouRequest.TYPE_RICH)
        assert_in('interation=458754%2C458756', url)
