# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import requests

from wechatsogou.pkgs import readimg, input
from wechatsogou.filecache import WechatCache

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
