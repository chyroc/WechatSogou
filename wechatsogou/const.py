# -*- coding: utf-8 -*-

from functools import wraps

from wechatsogou.exceptions import WechatSogouException


def Const(cls):
    @wraps(cls)
    def new_setattr(self, name, value):
        raise WechatSogouException('const : {} can not be changed'.format(name))

    cls.__setattr__ = new_setattr
    return cls


@Const
class _WechatSogouSearchArticleTypeConst(object):
    all = 'all'
    rich = 'rich'
    video = 'video'
    image = 'image'


@Const
class _WechatSogouSearchArticleTimeConst(object):
    """搜索条件 时间

    0 没有限制 / 1一天 / 2一周 / 3一月 / 4一年 / 5自定
    """
    anytime = 0
    day = 1
    week = 2
    month = 3
    year = 4
    specific = 5


@Const
class _WechatSogouHotIndexConst(object):
    hot = 'hot'
    recommendation = 'recommendation'
    duanzi = 'duanzi'
    health = 'health'
    sifanghua = 'sifanghua'
    gossip = 'gossip'
    life = 'life'
    finance = 'finance'
    car = 'car'
    technology = 'technology'
    fashion = 'fashion'
    mummy = 'mummy'
    dianzan = 'dianzan'
    travel = 'travel'
    job = 'job'
    food = 'food'
    history = 'history'
    study = 'study'
    constellation = 'constellation'
    sport = 'sport'


@Const
class _Const(object):
    hot_index = _WechatSogouHotIndexConst()
    search_article_type = _WechatSogouSearchArticleTypeConst()
    search_article_time = _WechatSogouSearchArticleTimeConst()


WechatSogouConst = _Const()
