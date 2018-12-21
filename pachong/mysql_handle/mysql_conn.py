#!/usr/bin/python3

import pymysql


class MySqlConn(object):
    # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

    @staticmethod
    def get_mysql():
        # 打开数据库连接
        mysql_conn = pymysql.connect("localhost", "dev", "dev123456", "dm")
        return mysql_conn

    @staticmethod
    def get_mysql_version():
        mysql_conn = MySqlConn.get_mysql()

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = mysql_conn.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()

        print("Database version : %s " % data)

        # 关闭数据库连接
        mysql_conn.close()


if __name__ == '__main__':
    print("-------------------")
    MySqlConn.get_mysql_version()
