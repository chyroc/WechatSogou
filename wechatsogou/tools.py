# -*- coding: utf-8 -*-

import json

import requests

try:
    import urlparse as url_parse
except ImportError:
    import urllib.parse as url_parse


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


def get_encoding_from_reponse(r):
    """获取requests库get或post返回的对象编码

    Args:
        r: requests库get或post返回的对象

    Returns:
        对象编码
    """
    encoding = requests.utils.get_encodings_from_content(r.text)
    return encoding[0] if encoding else requests.utils.get_encoding_from_headers(r.headers)


def _replace_html(s):
    """替换html‘&quot;’等转义内容为正常内容

    Args:
        s: 文字内容

    Returns:
        s: 处理反转义后的文字
    """
    s = s.replace('&#39;', '\'')
    s = s.replace('&quot;', '"')
    s = s.replace('&amp;', '&')
    s = s.replace('&gt;', '>')
    s = s.replace('&lt;', '<')
    s = s.replace('&yen;', '¥')
    s = s.replace('amp;', '')
    s = s.replace('&lt;', '<')
    s = s.replace('&gt;', '>')
    s = s.replace('&nbsp;', ' ')
    s = s.replace('\\', '')
    return s


def _replace_dict(dicts):
    retu_dict = dict()
    for k, v in dicts.items():
        retu_dict[replace_all(k)] = replace_all(v)
    return retu_dict


def _replace_list(lists):
    retu_list = list()
    for l in lists:
        retu_list.append(replace_all(l))
    return retu_list


def replace_all(data):
    if isinstance(data, dict):
        return _replace_dict(data)
    elif isinstance(data, list):
        return _replace_list(data)
    elif isinstance(data, str):
        return _replace_html(data)
    else:
        return data


def str_to_dict(json_str):
    json_dict = eval(json_str)
    return replace_all(json_dict)


def replace_space(s):
    s = s.replace(' ', '')
    s = s.replace('\r\n', '')
    return s


def get_url_param(url):
    result = url_parse.urlparse(url)
    return url_parse.parse_qs(result.query, True)


def input(msg=''):
    try:
        return raw_input(msg)
    except NameError:
        return input(msg)


if __name__ == '__main__':
    aa = list_or_empty(['list'])
    print(aa, type(aa))
