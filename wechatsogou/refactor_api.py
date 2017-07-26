# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import time

import requests

from wechatsogou.pkgs import readimg, input, quote
from wechatsogou.refactor_request import WechatSogouRequest
from wechatsogou.refactor_structuring import WechatSogouStructuring
from wechatsogou.exceptions import WechatSogouRequestsExceptionRefactor


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
    def search_gzh(self, keyword, page=1, callback=None):
        """搜索 公众号

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1

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
        r = WechatSogouRequest.get(url, req=req)

        if not r.ok:
            raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI.search_gzh', r)

        # if '用户您好，您的访问过于频繁，为确认本次访问为正常用户行为，需要您协助验证' in r.text:
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
                    print(j)

        headers = {
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'weixin.sogou.com',
            'Referer': r.url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Upgrade-Insecure-Requests': '1'
        }
        print(url)
        # r = WechatSogouRequest.get(url, req=req, headers=headers)
        r = req.get(url, headers=headers)
        print('返回')
        print(r)
        print(r.url)
        print(r.history)
        print(r.encoding)
        print(r.headers)

        return WechatSogouStructuring.get_gzh_by_search(r.text)
