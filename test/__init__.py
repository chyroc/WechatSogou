# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import os

from wechatsogou.request import WechatSogouRequest
from wechatsogou.structuring import WechatSogouStructuring

ws = WechatSogouRequest()
ws_structuring = WechatSogouStructuring()

gaokao_keyword = '高考'
fake_data_path = '{}/file'.format(os.getcwd() if 'test' in os.getcwd() else '{}/test'.format(os.getcwd()))
