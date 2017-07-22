# -*- coding: utf-8 -*-

try:
    from urllib.request import quote as quote
except ImportError:
    from urllib import quote as quote
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')

import requests


class WechatSogouBasic(object):
    def __init__(self):
        pass

    @staticmethod
    def _gen_search_url(query, type, page=1, timesn=None, interation=None, wxid=None, usip=None, ft=None):
        """ 拼接搜索URL

        :param query:      搜索文字
        :param type:       类型 1 是公号 2 是文章
        :param timesn:     时间 1一天 / 2一周 / 3一月 / 4一年 / 5自定
        :param ft:         当 tsn 是 5 时，本参数代表时间 ['', '']
        :param interation: 含有内容的类型 458754 有图 / 458756 有视频
        :param wxid
        :param usip        联合起来就是账号内搜索
        :return:
        """
        """
        账号 http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=3&ft=&et=&interation=458754&wxid=oIWsFt1tmWoG6vO6BcsS7St61bRE&usip=nanhangqinggong

        一天 http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=1&ft=&et=&interation=&wxid=&usip=
        一周 http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=2&ft=&et=&interation=&wxid=&usip=
        一月 http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=3&ft=&et=&interation=&wxid=&usip=
        一年 http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=4&ft=&et=&interation=&wxid=&usip=
        自定 http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=5&ft=2017-07-01&et=2017-07-15&interation=&wxid=&usip=

        类型
            http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=3&ft=&et=&interation=&wxid=&usip=
            http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=3&ft=&et=&interation=458754&wxid=&usip=
            http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%AB%98%E8%80%83&tsn=3&ft=&et=&interation=458754%2C458756&wxid=&usip=
        """
        # TODO 账号内搜索
        assert type in [1, 2]

        url = 'http://weixin.sogou.com/weixin?type={}&ie=utf8&query={}'.format(type, quote(query))

        if type == 1:
            return url
        return url

    def _search(self, query, type, page=1, timesn=None, interation=None, wxid=None, usip=None, ft=None):
        url = WechatSogouBasic._gen_search_url(query, type, page, timesn, interation, wxid, usip, ft)
        r = requests.get(url)
        if not r.ok:
            # todo 错误处理
            return None
        return r.text
