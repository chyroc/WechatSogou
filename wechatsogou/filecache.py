# -*- coding: utf-8 -*-

from werkzeug.contrib.cache import FileSystemCache


class WechatCache(object):
    """基于文件的缓存

    """

    def __init__(self, cache_dir='cache', default_timeout=300):
        """初始化

        cache_dir是缓存目录
        """
        self.cache = FileSystemCache(cache_dir, default_timeout=default_timeout)

    def clear(self):
        """清空缓存
        """
        return self.cache.clear()

    def get(self, key):
        """获取缓存

        获取键值key的缓存值
        如果没有对应缓存，返回None
        """
        return self.cache.get(key)

    def add(self, key, value, timeout=None):
        """增加缓存

        如果键值key对应的缓存不存在，那么增加值value到键值key，过期时间timeout，默认300秒
        否则返回False（即不能覆盖设置缓存）
        """
        return self.cache.add(key, value, timeout)

    def set(self, key, value, timeout=None):
        """设置缓存

        设置键值key的缓存为value,过期时间300秒
        """
        return self.cache.set(key, value, timeout)

    def delete(self, key):
        """删除缓存

        删除键值key存储的缓存
        """
        return self.cache.delete(key)


if __name__ == '__main__':
    cache = WechatCache()
    import requests

    r = requests.session()
    print(cache.set('1', r))
    print(cache.get('1'), type(cache.get('1')))
