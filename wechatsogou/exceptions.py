# -*- coding: utf-8 -*-


class WechatSogouException(Exception):
    """基于搜狗搜索的的微信公众号爬虫接口  异常基类
    """
    pass


class WechatSogouVcodeException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 出现验证码 异常类
    """
    pass


class WechatSogouVcodeOcrException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 验证码 识别错误 异常类
    """
    pass


class WechatSogouJsonException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 非标准json数据 异常类
    """
    pass


class WechatSogouEndException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 数据处理完成 异常类
    """
    pass


class WechatSogouBreakException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 中断 异常类
    """
    pass


class WechatSogouHistoryMsgException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 数据处理完成 异常类
    """
    pass


class ConfigException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 配置错误 异常类
    """
    pass


class WechatSogouRequestsException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 抓取 异常类
    """

    def __init__(self, errmsg, status_code):
        WechatSogouException(errmsg)
        self.status_code = status_code
