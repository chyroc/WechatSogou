# -*- coding: utf-8 -*-

# __        __        _           _   ____
# \ \      / /__  ___| |__   __ _| |_/ ___|  ___   __ _  ___  _   _
#  \ \ /\ / / _ \/ __| '_ \ / _` | __\___ \ / _ \ / _` |/ _ \| | | |
#   \ V  V /  __/ (__| | | | (_| | |_ ___) | (_) | (_| | (_) | |_| |
#    \_/\_/ \___|\___|_| |_|\__,_|\__|____/ \___/ \__, |\___/ \__,_|
#                                                 |___/

"""
WechatSogou Crawler Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from wechatsogou.api import WechatSogouAPI
from wechatsogou.const import WechatSogouConst
from wechatsogou.request import WechatSogouRequest
from wechatsogou.structuring import WechatSogouStructuring
from wechatsogou.exceptions import WechatSogouException, WechatSogouVcodeOcrException, WechatSogouRequestsException

__all__ = [
    'WechatSogouConst',

    'WechatSogouAPI',
    'WechatSogouRequest',
    'WechatSogouStructuring',

    'WechatSogouException',
    'WechatSogouVcodeOcrException',
    'WechatSogouRequestsException']

__title__ = 'wechatsogou'
__version__ = "4.0.2"
__author__ = 'Chyroc'

"""doc string

https://www.jetbrains.com/help/pycharm/type-hinting-in-pycharm.html
https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
"""
