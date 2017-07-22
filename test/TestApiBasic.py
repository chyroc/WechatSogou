import os
import unittest
from nose.tools import assert_raises, assert_equal

import requests_mock

from api.basic import WechatSogouBasic


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.ws = WechatSogouBasic()

    def test_gen_search_url(self):
        assert_equal(WechatSogouBasic._gen_search_url('高考', 1),
                     'http://weixin.sogou.com/weixin?type=1&ie=utf8&query=%E9%AB%98%E8%80%83')
        assert_equal(WechatSogouBasic._gen_search_url('高考', 2),
                     'http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83')
        with assert_raises(AssertionError):
            assert_equal(WechatSogouBasic._gen_search_url('高考', 3),
                         'http://weixin.sogou.com/weixin?type=3&ie=utf8&query=%E9%AB%98%E8%80%83')

    @requests_mock.mock()
    def test_search_article(self, m):
        file = '{}/{}'.format(os.getcwd(), 'file/search-gaokao-article.html')
        with open(file) as f:
            search_gaokao_article = f.read()
            m.get(WechatSogouBasic._gen_search_url('高考', 2), text=search_gaokao_article)
        text = self.ws._search('高考', 2)
        assert_equal(text, search_gaokao_article)


if __name__ == '__main__':
    unittest.main()
