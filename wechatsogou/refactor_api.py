# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import time

import requests

from wechatsogou.pkgs import readimg, input
from wechatsogou.refactor_request import WechatSogouRequest
from wechatsogou.refactor_structuring import WechatSogouStructuring
from wechatsogou.filecache import WechatCache
from wechatsogou.exceptions import WechatSogouRequestsExceptionRefactor, WechatSogouVcodeOcrException

ws_cache = WechatCache()


def identify_image_callback_example(img):
    """识别二维码

    Parameters
    ----------
    img : bytes
        验证码图片二进制数据

    Returns
    -------
    str
        验证码文字
    """
    im = readimg(img)
    im.show()
    return input("please input code: ")


def deblocking_callback_example(url, req, resp, img, identify_image_callback):
    """手动打码解锁

    Parameters
    ----------
    url : str or unicode
        验证码页面 之前的 url
    req : requests.sessions.Session
        requests.Session() 供调用解锁
    resp : requests.models.Response
        requests 访问页面返回的，已经跳转了
    img : bytes
        验证码图片二进制数据
    identify_image_callback : callable
        处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

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
    # no use resp
    url_quote = url.split('weixin.sogou.com/')[-1]

    img_code = identify_image_callback(img)
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

    return r_deblocking.json()


class WechatSogouAPI(object):
    def __set_cookie(self, suv=None, snuid=None):
        suv = ws_cache.get('suv') if suv is None else suv
        snuid = ws_cache.get('snuid') if snuid is None else snuid

        return {'Cookie': 'SUV={};SNUID={};'.format(suv, snuid)}

    def __set_cache(self, suv, snuid):
        ws_cache.set('suv', suv)
        ws_cache.set('snuid', snuid)

    def __deblocking_search(self, url, resp, req, deblocking_callback, identify_image_callback):
        millis = int(round(time.time() * 1000))
        r_img = req.get('http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(millis))
        if not r_img.ok:
            raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI get img', resp)

        if callable(deblocking_callback):
            r_deblocking = deblocking_callback(req, resp, r_img.content)
        else:
            if callable(identify_image_callback):
                r_deblocking = deblocking_callback_example(url, req, resp, r_img.content,
                                                           identify_image_callback=identify_image_callback)
            else:
                r_deblocking = deblocking_callback_example(url, req, resp, r_img.content,
                                                           identify_image_callback=identify_image_callback_example)

        if r_deblocking['code'] != 0:
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {code}, msg: {msg}'.format(**r_deblocking))
        else:
            self.__set_cache(req.cookies.get('SUID'), r_deblocking['id'])

    def get_gzh_info(self, wecgat_id_or_name, deblocking_callback=None, identify_image_callback=None):
        """获取公众号微信号 wechatid 的信息

        因为wechatid唯一确定，所以第一个就是要搜索的公众号

        Parameters
        ----------
        wecgat_id_or_name : str or unicode
            wechat_id or wechat_name
        deblocking_callback : callable
            处理出现验证码页面的函数，参见 deblocking_callback_example
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        dict or None
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
        info = self.search_gzh(wecgat_id_or_name)
        return info[0] if info else None

    def search_gzh(self, keyword, page=1, deblocking_callback=None, identify_image_callback=None):
        """搜索 公众号

        对于出现验证码的情况，可以由使用者自己提供：
            1、函数 deblocking_callback ，这个函数 handle 出现验证码到解决的整个流程
            2、也可以 只提供函数 identify_image_callback，这个函数输入验证码二进制数据，输出验证码文字，剩下的由 wechatsogou 包来解决
        注意：
            函数 deblocking_callback 和 identify_image_callback 只需要提供一个，如果都提供了，那么 identify_image_callback 不起作用

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1
        deblocking_callback : callable
            处理出现验证码页面的函数，参见 deblocking_callback_example
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

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
        resp = WechatSogouRequest.get(url, req=req, headers=self.__set_cookie())

        if not resp.ok:
            raise WechatSogouRequestsExceptionRefactor('WechatSogouAPI.search_gzh', resp)

        if 'antispider' in resp.url:
            self.__deblocking_search(url, resp, req, deblocking_callback, identify_image_callback)

        headers = self.__set_cookie()
        r = WechatSogouRequest.get(url, req=req, headers=headers)  # req=req

        return WechatSogouStructuring.get_gzh_by_search(r.text)
