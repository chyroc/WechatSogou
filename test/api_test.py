# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

import wechatsogou
from test import config


class ApiTest(unittest.TestCase):
    def setUp(self):
        ocr_config = {
            'type': 'ruokuai',
            'dama_name': config.username,
            'dama_pswd': config.password,
            'dama_soft_id': config.soft_id,
            'dama_soft_key': config.soft_key
        }
        self.api = wechatsogou.WechatSogouApi(ocr_config=ocr_config)

    def test_search_gzh_info(self):
        name = '南京航空航天大学'
        wechat_infos = self.api.search_gzh_info(name)
        wechat_name = [wechat_info['name'] for wechat_info in wechat_infos]
        assert name in wechat_name


if __name__ == '__main__':
    unittest.main()
