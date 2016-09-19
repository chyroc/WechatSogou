# -*- coding: utf-8 -*-

import pymysql
from . import config


class DbException(Exception):
    """数据库 异常 基类
    """
    pass


class MysqlDbException(DbException):
    """数据库 myslq 异常类
    """
    pass


class mysql():
    """数据库类

    例子
    m = M('user')
    m.table('user').add({}) # 插入
    m.table('user').where({}).save({}) # 更新
    m.table('user').field(['id']).where({}).order({'id':'desc'}).find() # 读取，asc，desc
    m.where({}).delete() # 删除
    """

    def __init__(self, table='', prefix=''):
        """初始化

        table是初始化选择的表，后面可以使用table()函数更改
        prefix是数据表前缀，一般配置在config中
        """
        self.host = config.host
        self.user = config.user
        self.passwd = config.passwd
        self.db = config.db
        self.charset = config.charset
        if prefix:
            self.prefix = prefix + '_'
        elif config.prefix:
            self.prefix = config.prefix + '_'
        else:
            self.prefix = ''
        if table:
            self.tablename = self.prefix + table
        self.__conn()

    def __conn(self):
        """连接数据库函数
        """
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db,
                                    charset=self.charset, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        return self

    def __update(self, sqls):
        """更新语句，可执行update,insert语句
        """
        if type(sqls) is str:
            sta = self.cur.execute(sqls)
        elif type(sqls) is list:
            for sql in sqls:
                sta = self.cur.execute(sql)
        else:
            raise MysqlDbException('更新语句参数错误 - Model.__update')
        self.conn.commit()

    def __delete(self, sql):
        """删除语句
        """
        return self.cur.execute(sql)

    def __query(self, sql):
        """查询语句
        """
        return self.cur.execute(sql)

    def __close(self):
        """关闭所有连接
        """
        self.cur.close()
        self.conn.close()

    def __del__(self):
        """析构函数
        """
        self.conn.commit()
        self.__close()

    """
    以下是封装的提供使用的
    """

    def table(self, table, prefix=''):
        """设置数据表, 链式操作
        """
        if prefix:
            prefix = prefix + '_'
        elif hasattr(self, 'prefix'):
            prefix = self.prefix
        else:
            prefix = ''
        self.tablename = prefix + table
        return self

    def limit(self, pre, count):
        self.limit_sql = 'limit ' + str(pre) + ',' + str(count)
        return self

    def where(self, where):
        """设置条件, 链式操作
        """
        if type(where) is str:
            raise MysqlDbException('请输入字典 - Model.where')
            # self.where_sql = where
        elif type(where) is dict:
            where_sql = ''
            for k, v in where.items():
                where_sql += "`" + str(k) + "` LIKE '" + str(v) + "' and "
            self.where_sql = where_sql[:-5]
        return self

    def field(self, field):
        """设置操作的字段
        """
        if type(field) is str:
            if field == '*':
                self.field_sql = "*"
            else:
                self.field_sql = "`" + field + "`"
        elif type(field) is list:
            field_dian = []
            for f in field:
                field_dian.append("`" + f + "`")
            self.field_sql = ','.join(field_dian)
        else:
            raise MysqlDbException('field参数不是字符或者列表 - Model.field')
        return self

    def order(self, order):
        """排序
        """
        if type(order) is dict:
            for k, v in order.items():
                self.order_sql = " order by `" + k + "` " + v
                break
        else:
            raise MysqlDbException('排序参数不是字典 - Model.order')
        return self

    def add(self, data):
        """插入数据
        """
        ks = ''
        vs = ''
        for k, v in data.items():
            ks += "`" + str(k).replace('\'', '\\\'') + "`,"
            vs += "'" + str(v).replace('\'', '\\\'') + "',"
        if hasattr(self, 'tablename'):
            sql = "insert into `" + self.tablename + "` (" + ks[:-1] + ") values (" + vs[:-1] + ")"
            try:
                self.__update(sql)
            except pymysql.err.IntegrityError:
                pass
        else:
            raise MysqlDbException('缺少数据表 - Model.add')

    def save(self, data):
        """更新数据
        """
        if not hasattr(self, 'where_sql'):
            raise MysqlDbException('缺少where语句 - Model.save')
        if not hasattr(self, 'tablename'):
            raise MysqlDbException('缺少tablename - Model.save')
        data_sql = ''
        for k, v in data.items():
            data_sql += "`" + str(k) + "` = '" + str(v) + "',"
        sql = "update `" + self.tablename + "` set " + data_sql[:-1] + " where " + self.where_sql + ";"
        self.__update(sql)

    def find(self, size=25):
        """查询数据
        """
        where_sql = " where " + self.where_sql if hasattr(self, 'where_sql') else ""
        field_sql = self.field_sql if hasattr(self, 'field_sql') else "*"
        order_sql = self.order_sql if hasattr(self, 'order_sql') else ""
        limit_sql = self.limit_sql if hasattr(self, 'limit_sql') else ""
        sql = "select " + field_sql + " from `" + self.tablename + "`" + where_sql + order_sql + limit_sql
        self.__query(sql)
        if size == 0:
            return self.cur.fetchall()
        elif size == 1:
            return self.cur.fetchone()
        else:
            return self.cur.fetchmany(size)

    def delete(self):
        """删除语句
        """
        sql = "DELETE FROM `liaa_user` WHERE `id`='3'"
        return self.__delete(sql)


if __name__ == '__main__':
    pass
