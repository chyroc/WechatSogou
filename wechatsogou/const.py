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
    hot = 'hot'  # 热门
    gaoxiao = 'gaoxiao'  # 搞笑
    health = 'health'  # 养生
    sifanghua = 'sifanghua'  # 私房话
    gossip = 'gossip'  # 八卦
    technology = 'technology'  # 科技
    finance = 'finance'  # 财经
    car = 'car'  # 汽车
    life = 'life'  # 生活
    fashion = 'fashion'  # 时尚
    mummy = 'mummy'  # 辣妈 / 育儿
    travel = 'travel'  # 旅行
    job = 'job'  # 职场
    food = 'food'  # 美食
    history = 'history'  # 历史
    study = 'study'  # 学霸 / 教育
    constellation = 'constellation'  # 星座
    sport = 'sport'  # 体育
    military = 'military'  # 军事
    game = 'game'  # 游戏
    pet = 'pet'  # 萌宠


@Const
class _Const(object):
    hot_index = _WechatSogouHotIndexConst()
    search_article_type = _WechatSogouSearchArticleTypeConst()
    search_article_time = _WechatSogouSearchArticleTimeConst()


WechatSogouConst = _Const()
