# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import time

import requests

from wechatsogou.pkgs import readimg, input, quote
from wechatsogou.refactor_request import WechatSogouRequest
from wechatsogou.refactor_structuring import WechatSogouStructuring
from wechatsogou.filecache import WechatCache
from wechatsogou.exceptions import WechatSogouRequestsExceptionRefactor

ws_cache = WechatCache()


def deblocking_search(url, req, r, img):
    """手动打码解锁

    Parameters
    ----------
    url : str or unicode
        url
    req : requests.sessions.Session
        requests.Session() 供调用解锁
    r : requests.models.Response
        requests 访问页面返回的，已经跳转了
    img : bytes
        验证码图片二进制数据

    Returns
    -------
    dict
        {
            'url': '',
            'img': '',
            'name': '',
            'wechat_id': '',
            'post_perm': '',
            'qrcode': '',
            'introduction': '',
            'authentication': ''
        }
    """
    # no use r
    url_quote = url.split('weixin.sogou.com/')[-1]

    im = readimg(img)
    im.show()
    img_code = input("please input code: ")
    deblocking_url = 'http://weixin.sogou.com/antispider/thank.php'
    data = {
        'c': img_code,
        'r': '%2F' + url_quote,
        'v': 5
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + url_quote
    }
    r_deblocking = req.post(deblocking_url, data, headers=headers)
    if not r_deblocking.ok:
        pass

    deblocking_json = r_deblocking.json()

    print(r_deblocking.content)

    return deblocking_json


class WechatSogouAPI(object):
    def __set_cookie(self, suv=None, snuid=None):
        suv = ws_cache.get('suv') if suv is None else suv
        snuid = ws_cache.get('snuid') if snuid is None else snuid

        return {'Cookie': 'SUV={};SNUID={};'.format(suv, snuid)}

    def __set_cache(self, suv, snuid):
        ws_cache.set('suv', suv)
        ws_cache.set('snuid', snuid)

    def search_gzh(self, keyword, page=1, callback=None):
        """搜索 公众号

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1
        callback : function
            处理验证码的函数，参见 deblocking_search

        Returns
        -------
        list[dict]
            {
                'url': '',
                'img': '',
                'name': '',
                'wechat_id': '',
                'post_perm': '',
                'qrcode': '',
                'introduction': '',
                'authentication': ''
            }

        Raises
        ------
        WechatSogouRequestsException
            requests error
        """
        req = requests.session()

        url = WechatSogouRequest._gen_search_gzh_url(keyword, page)
        r = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie())

        if not r.ok:
            raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI.search_gzh', r)

        if 'antispider' in r.url:
            millis = int(round(time.time() * 1000))
            r_img = req.get('http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(millis))
            if not r_img.ok:
                raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI.search_gzh', r)

            if callable(callback):
                callback(req, r, r_img.content)  # TODO doc
            else:
                j = deblocking_search(url, req, r, r_img.content)
                if j['code'] != 0:
                    raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI.search_gzh', r)
                else:
                    self.__set_cache(req.cookies.get('SUID'), j['id'])

        headers = self.__set_cookie()
        r = WechatSogouRequest.get(url, headers=headers)  # req=req
        print(r.url)

        return WechatSogouStructuring.get_gzh_by_search(r.text)
