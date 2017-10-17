# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import ast

import requests

from wechatsogou.five import url_parse


def list_or_empty(content, contype=None):
    assert isinstance(content, list), 'content is not list: {}'.format(content)

    if content:
        return contype(content[0]) if contype else content[0]
    else:
        if contype:
            if contype == int:
                return 0
            elif contype == str:
                return ''
            elif contype == list:
                return []
            else:
                raise Exception('only can deal int str list')
        else:
            return ''


def get_elem_text(elem):
    """抽取lxml.etree库中elem对象中文字

    Args:
        elem: lxml.etree库中elem对象

    Returns:
        elem中文字
    """
    return ''.join([node.strip() for node in elem.itertext()])


def get_first_of_element(element, sub, contype=None):
    """抽取lxml.etree库中elem对象中文字

    Args:
        element: lxml.etree.Element
        sub: str

    Returns:
        elem中文字
    """
    content = element.xpath(sub)
    return list_or_empty(content, contype)


def get_encoding_from_reponse(r):
    """获取requests库get或post返回的对象编码

    Args:
        r: requests库get或post返回的对象

    Returns:
        对象编码
    """
    encoding = requests.utils.get_encodings_from_content(r.text)
    return encoding[0] if encoding else requests.utils.get_encoding_from_headers(r.headers)


def _replace_str_html(s):
    """替换html‘&quot;’等转义内容为正常内容

    Args:
        s: 文字内容

    Returns:
        s: 处理反转义后的文字
    """
    html_str_list = [
        ('&#39;', '\''),
        ('&quot;', '"'),
        ('&amp;', '&'),
        ('&yen;', '¥'),
        ('amp;', ''),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&nbsp;', ' '),
        ('\\', '')
    ]
    for i in html_str_list:
        s = s.replace(i[0], i[1])
    return s


def replace_html(data):
    if isinstance(data, dict):
        return dict([(replace_html(k), replace_html(v)) for k, v in data.items()])
    elif isinstance(data, list):
        return [replace_html(l) for l in data]
    elif isinstance(data, str) or isinstance(data, unicode):
        return _replace_str_html(data)
    else:
        return data


def str_to_dict(json_str):
    json_dict = ast.literal_eval(json_str)
    return replace_html(json_dict)


def replace_space(s):
    return s.replace(' ', '').replace('\r\n', '')


def get_url_param(url):
    result = url_parse.urlparse(url)
    return url_parse.parse_qs(result.query, True)
