# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import io
import os
import unittest
from nose.tools import assert_equal, assert_not_equal

import httpretty

from wechatsogou.refactor_request import WechatSogouRequest
from test.test_main import gaokao_keyword, fake_data_path


class TestBasicSearchArticle(unittest.TestCase):
    @httpretty.activate
    def test_search_article_keyword(self):
        url = WechatSogouRequest._gen_search_article_url(gaokao_keyword)
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'search-gaokao-article.html')
        with io.open(file_name, encoding='utf-8') as f:
            search_gaokao_article = f.read()
            httpretty.register_uri(httpretty.GET, url, body=search_gaokao_article)

        r = WechatSogouRequest._search_article(gaokao_keyword)
        assert_equal(search_gaokao_article, r.text)
        assert_equal(url, r.url)
        assert_not_equal(WechatSogouRequest._gen_search_article_url(gaokao_keyword, 2), r.url)
        assert_not_equal(WechatSogouRequest._search_gzh(gaokao_keyword), r.url)


class TestBasicSearchGzh(unittest.TestCase):
    @httpretty.activate
    def test_search_gzh_keyword(self):
        url = WechatSogouRequest._gen_search_gzh_url(gaokao_keyword)
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'search-gaokao-gzh.html')
        with io.open(file_name, encoding='utf-8') as f:
            search_gaokao_gzh = f.read()
            httpretty.register_uri(httpretty.GET, url, body=search_gaokao_gzh)

        r = WechatSogouRequest._search_gzh(gaokao_keyword)
        assert_equal(search_gaokao_gzh, r.text)
        assert_equal(url, r.url)
        assert_not_equal(WechatSogouRequest._search_gzh(gaokao_keyword, 2), r.url)
        assert_not_equal(WechatSogouRequest._search_article(gaokao_keyword), r.url)


if __name__ == '__main__':
    unittest.main()
