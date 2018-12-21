#!/usr/bin/python
#encoding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import time
import json

from mysql_handle.mysql_conn import MySqlConn


class AreaCodeParse(object):

    html_file_path = '/Users/xxxs/Documents/dev-code/html_area_zip_code.txt'
    html_file_parsed_path = '/Users/xxxs/Documents/dev-code/html_area_zip_code_parsed.txt'

    def request_url(self, date_time_str):
        url = "http://202.108.98.30/defaultQuery?defaultQuery?shengji=&diji=-1&xianji="

        headers = {  # 请求头请求刷新验证码和发送post时需要使用
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate'
        }

        print("get_area_zip_code stat...")
        session = requests.Session()
        print("get_area_zip_code-url-is:", url)

        res = session.get(url, headers=headers)

        # 设置编码
        data = res.content.decode("GBK", "ignore")
        self.soup_from_html(data)

    def file_write(self, path, content):
        target_file = open(path + date_time_str, 'w')
        target_file.write(content)
        target_file.close()

    def soup_parse(self, content):
        soup = BeautifulSoup(content, "html.parser")
        info_table = soup.find("table", {"class": "info_table"})

        tr_lines = info_table.find_all("tr")

        print(date_time_str)

        ## 写文件
        html_file_parsed = open(self.html_file_parsed_path + date_time_str, 'wb')

        for tr_line in tr_lines:
            if len(tr_line) > 0:
                pretty = tr_line.prettify()
                new_tr = re.sub('\r?\n', '', pretty) + "\n"
                html_file_parsed.write(new_tr.encode("utf-8"))
        html_file_parsed.close()

    def soup_parse2(self, content):
        soup = BeautifulSoup(content, "html.parser")

        input_hidden_value = soup.find("input", {"id": "pyArr"})['value'].replace(" ", "")

        datas = json.loads(input_hidden_value)

        mysql_conn = MySqlConn.get_mysql()

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = mysql_conn.cursor()

        for data in datas:
            # {'cName': '北京市', 'code': '110000', 'py': 'BeijingShi', 'jp': 'bjs', 'qp': 'BeijingShi'}
            # {'cName': '北京市', 'code': '110000', 'py': 'BeijingShi', 'jp': 'bjs', 'qp': 'BeijingShi'}
            self.insert_into_mysql(mysql_conn, cursor, (data['cName'], data['code'], data['py'], data['jp'], data['qp']))

        cursor.close()
        mysql_conn.close()

    def soup_from_html(self, content):
        # self.soup_parse(content)
        self.soup_parse2(content)

    def soup_from_text(self, date_time_str):
        # python file doc: https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html
        text_file = open(self.html_file_path + date_time_str, encoding="utf-8")
        content = text_file.read()
        self.soup_parse(content)

    def parse_element(self, tree):
        items = tree.xpath('//*[@id="center"]/div[3]/table[@class="info_table"]')

        print(items)

        print(items[0])
        for item in items:
            print("\n====>>")
            print(item.element())

        ## 写文件
        target_file2 = open('/Users/xxxs/Documents/dev-code/html_area_zip_code_res.txt', 'w')
        target_file2.write(items)
        target_file2.close()

    def insert_into_mysql(self, mysql_conn, cursor, data):
        insert_sql = ("INSERT INTO dim_city_name_code (cName,code,py,jp, qp) VALUES (%s, %s, %s, %s, %s)")

        # 使用 execute()  方法执行 SQL 查询
        try:
            cursor.execute(insert_sql, data)
            mysql_conn.commit()

        except Exception as e:
            mysql_conn.rollback()
            print(str(e))


if __name__ == '__main__':
    print("-------------------")
    parse = AreaCodeParse()
    # date_time_str = time.strftime("%Y-%m-%d%H:%M:%S", time.localtime())
    date_time_str = "_" + time.strftime("%Y-%m-%d-%H", time.localtime())
    parse.request_url(date_time_str)

