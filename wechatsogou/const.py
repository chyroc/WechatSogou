from functools import wraps

from wechatsogou.exceptions import WechatSogouException


def Const(cls):
    @wraps(cls)
    def new_sett(self, name, value):
        raise WechatSogouException('const : {} can not be changed'.format(name))

    cls.__setattr__ = new_sett
    return cls


@Const
class _WechatSogouSearchArticleTypeConst(object):
    all = 'all'
    rich = 'rich'
    video = 'video'
    image = 'image'


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


WechatSogouConst = _Const()
