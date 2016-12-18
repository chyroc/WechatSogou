# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

import wechatsogou
import env_variable


class ApiTest(unittest.TestCase):
    def setUp(self):
        ocr_config = {
            'type': 'ruokuai',
            'dama_name': env_variable.username,
            'dama_pswd': env_variable.password,
            'dama_soft_id': env_variable.soft_id,
            'dama_soft_key': env_variable.soft_key
        }
        self.api = wechatsogou.WechatSogouApi(ocr_config=ocr_config)

    def test_search_gzh_info(self):
        name = '南京航空航天大学'
        wechat_infos = self.api.search_gzh_info(name)
        wechat_name = [wechat_info['name'] for wechat_info in wechat_infos]
        assert name in wechat_name

    def test_get_gzh_info(self):
        wechat_id = 'nanhangqinggong'
        wechat_info = self.api.get_gzh_info(wechat_id)
        assert '南航青年志愿者' == wechat_info['name']

    def test_search_article_info(self):
        keywords = '马达数据与虎嗅F&M节的亲密接触'
        wechat_articles = self.api.search_article_info(keywords)
        times = [wechat_article['article']['time'] for wechat_article in wechat_articles]
        names = [wechat_article['gzh']['name'] for wechat_article in wechat_articles]
        assert 1481244814 in times
        assert '马达数据' in names

    def test_get_gzh_message(self):
        data = self.api.get_gzh_message(wechatid='madadata')
        assert len(data) > 2
        assert len(data[0]['title']) > 2

    def test_get_gzh_message_and_info(self):
        data_all = self.api.get_gzh_message_and_info(wechatid='madadata')
        assert '北京马达加科技有限公司' == data_all['gzh_info']['authentication']
        assert len(data_all['gzh_messages']) > 2
        assert len(data_all['gzh_messages'][0]['title']) > 2

    def test_get_recent_article_url_by_index_single(self):
        articles_single = self.api.get_recent_article_url_by_index_single()
        assert len(articles_single) == 20


if __name__ == '__main__':
    unittest.main()
