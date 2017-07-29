# -*- coding: utf-8 -*-

import unittest

from nose.tools import assert_true, assert_equal

from wechatsogou.const import WechatSogouConst


class TestConst(unittest.TestCase):
    def test_const_hot_index(self):
        assert_true(hasattr(WechatSogouConst, 'hot_index'))

        assert_equal(WechatSogouConst.hot_index.hot, 'hot')
        assert_equal(WechatSogouConst.hot_index.recommendation, 'recommendation')
        assert_equal(WechatSogouConst.hot_index.duanzi, 'duanzi')
        assert_equal(WechatSogouConst.hot_index.health, 'health')
        assert_equal(WechatSogouConst.hot_index.sifanghua, 'sifanghua')
        assert_equal(WechatSogouConst.hot_index.gossip, 'gossip')
        assert_equal(WechatSogouConst.hot_index.life, 'life')
        assert_equal(WechatSogouConst.hot_index.finance, 'finance')
        assert_equal(WechatSogouConst.hot_index.car, 'car')
        assert_equal(WechatSogouConst.hot_index.technology, 'technology')
        assert_equal(WechatSogouConst.hot_index.fashion, 'fashion')
        assert_equal(WechatSogouConst.hot_index.mummy, 'mummy')
        assert_equal(WechatSogouConst.hot_index.dianzan, 'dianzan')
        assert_equal(WechatSogouConst.hot_index.travel, 'travel')
        assert_equal(WechatSogouConst.hot_index.job, 'job')
        assert_equal(WechatSogouConst.hot_index.food, 'food')
        assert_equal(WechatSogouConst.hot_index.history, 'history')
        assert_equal(WechatSogouConst.hot_index.study, 'study')
        assert_equal(WechatSogouConst.hot_index.constellation, 'constellation')
        assert_equal(WechatSogouConst.hot_index.sport, 'sport')

    def test_const_search_article_type(self):
        assert_true(hasattr(WechatSogouConst, 'search_article_type'))

        assert_equal(WechatSogouConst.search_article_type.all, 'all')
        assert_equal(WechatSogouConst.search_article_type.rich, 'rich')
        assert_equal(WechatSogouConst.search_article_type.video, 'video')
        assert_equal(WechatSogouConst.search_article_type.image, 'image')

    def test_const_search_article_time(self):
        assert_true(hasattr(WechatSogouConst, 'search_article_time'))

        assert_equal(WechatSogouConst.search_article_time.anytime, 0)
        assert_equal(WechatSogouConst.search_article_time.day, 1)
        assert_equal(WechatSogouConst.search_article_time.week, 2)
        assert_equal(WechatSogouConst.search_article_time.month, 3)
        assert_equal(WechatSogouConst.search_article_time.year, 4)
        assert_equal(WechatSogouConst.search_article_time.specific, 5)


if __name__ == '__main__':
    unittest.main()
