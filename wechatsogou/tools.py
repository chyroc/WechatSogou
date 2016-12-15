# -*- coding: utf-8 -*-

import json


def prdict(content):
    msg = json.dumps(content, indent=1, ensure_ascii=False)
    print(msg)


def list_or_empty(content, contype=None):
    if isinstance(content, list):
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
                    raise Exception('only cna deal int str list')
            else:
                return ''
    else:
        raise Exception('need list')


if __name__ == '__main__':
    aa = list_or_empty(['list'])
    print(aa, type(aa))
