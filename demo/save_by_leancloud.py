# -*- coding: utf-8 -*-

import leancloud


class SaveLcoud(object):
    def __init__(self, **kwargs):

        appid = kwargs.get('appid')
        appkey = kwargs.get('appkey')
        if not appid and not appkey:
            raise Exception('need leancloud config')

        leancloud.init(appid, appkey)

    def save(self, tablename, datas):
        Table = leancloud.Object.extend(tablename)
        table_list = list()
        for data in datas:
            table = Table()
            for k, v in data.items():
                table.set(k, v)
            table_list.append(table)

        try:
            Table.save_all(table_list)
        except leancloud.errors.LeanCloudError:
            print('有重复.................')


if __name__ == '__main__':
    appid = ''
    appkey = ''

    tablename = ''
    datas = []

    sl = SaveLcoud(appid=appid, appkey=appkey)
    sl.save(tablename, datas)
