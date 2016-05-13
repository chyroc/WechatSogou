# -*- coding: UTF-8 -*-

import sqlite3
import os

class SqliteException(Exception):
    pass

class MySqlite(object):
    def __init__(self, path=''):
        """
        初始化, 链接数据库"""
        if path:
            self.db_path = path
        else:
            self.db_path = 'wechat.sqlite'
        self.conn()

    def conn(self):
        """
        链接数据库"""
        self.conn = sqlite3.connect(self.db_path)


    def create(self):
        raise SqliteException('cannot use create')

    def insert(self, table, data):
        if type(data) == dict:
            name = []
            value = []
            for k,v in data.items():
                name.append(k)
                value.append(v)
            sql_name = ','.join(str(v) for v in name)
            sql_value = '","'.join(str(v) for v in value)
            sql = 'INSERT INTO '+table+' ('+sql_name+') VALUES ("'+sql_value+'")'
            self.conn.execute(sql)
            self.conn.commit()
        else:
            raise SqliteException('data is not dict')

    def select(self, table, data):
        data_str = ','.join(str(v) for v in data)
        cursor = self.conn.execute('SELECT '+data_str+'  from '+table)
        return cursor

    def update(self, table, data_set, data_where):
        self.conn.execute('UPDATE '+table+' set SALARY = 25000.00 where ID=1')
        self.conn.commit()
