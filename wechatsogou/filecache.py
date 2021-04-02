# -*- coding: utf-8 -*-

try:
    from werkzeug.contrib.cache import FileSystemCache
except ImportError:
    from cachelib import FileSystemCache


class WechatCache(FileSystemCache):
    """基于文件的缓存

    """

    def __init__(self, cache_dir='/tmp/wechatsogou-cache', default_timeout=300):
        """初始化

        cache_dir是缓存目录
        """
        super(WechatCache, self).__init__(cache_dir, default_timeout)

    def get(self, key):
        try:
            return super(WechatCache, self).get(key)
        except ValueError:
            return None
