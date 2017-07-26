# -*- coding: utf-8 -*-


class WechatSogouException(Exception):
    """基于搜狗搜索的的微信公众号爬虫接口  异常基类
    """
    pass


class WechatSogouVcodeOcrException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 验证码 识别错误 异常类
    """
    pass


class WechatSogouRequestsException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 抓取 异常类

    Parameters
    ----------
    errmsg : str or unicode
        msg
    r : requests.models.Response
        return of requests
    """

    def __init__(self, errmsg, r):
        WechatSogouException('{} [url {}] [content {}]'.format(errmsg, r.url, r.content))
        self.status_code = r.status_code
