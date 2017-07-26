# -*- coding: utf-8 -*-

from werkzeug.contrib.cache import FileSystemCache


class WechatCache(FileSystemCache):
    """基于文件的缓存

    """

    def __init__(self, cache_dir='/tmp/wechatsogou-cache', default_timeout=300):
        """初始化

        cache_dir是缓存目录
        """
        super(WechatCache, self).__init__(cache_dir, default_timeout)
