# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

from wechatsogou.api import WechatSogouAPI
from wechatsogou.request import WechatSogouRequest
from wechatsogou.structuring import WechatSogouStructuring
from wechatsogou.exceptions import WechatSogouException, WechatSogouVcodeOcrException, WechatSogouRequestsException

__all__ = ['WechatSogouAPI', 'WechatSogouRequest', 'WechatSogouStructuring', 'WechatSogouException',
           'WechatSogouVcodeOcrException', 'WechatSogouRequestsException']

__version__ = "2.0.5"

"""doc string

https://www.jetbrains.com/help/pycharm/type-hinting-in-pycharm.html
https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
"""
