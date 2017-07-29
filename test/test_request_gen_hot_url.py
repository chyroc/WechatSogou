# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import unittest
from nose.tools import assert_in, assert_raises

from wechatsogou.const import WechatSogouConst
from wechatsogou.request import WechatSogouRequest


class TestBasicGenSearchArticleURL(unittest.TestCase):
    def test_gen_hot_url(self):
        for hot_index in filter(lambda x: not x.startswith('__'), dir(WechatSogouConst.hot_index)):
            url = WechatSogouRequest.gen_hot_url(hot_index)
            assert_in('http://weixin.sogou.com/wapindex/wap/0612/wap_', url)
            assert_in('0.html', url)

            with assert_raises(AssertionError):
                WechatSogouRequest.gen_hot_url(hot_index, 0)

            for page in range(1, 5):
                url = WechatSogouRequest.gen_hot_url(hot_index, page)
                assert_in('http://weixin.sogou.com/wapindex/wap/0612/wap_', url)
                assert_in('{}.html'.format(page - 1), url)


if __name__ == '__main__':
    unittest.main()
