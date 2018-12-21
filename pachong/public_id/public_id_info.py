#!/usr/bin/python
#encoding:utf-8

#
import sys, requests
from requests.compat import (quote, urlparse)
from bs4 import BeautifulSoup
import re

SAVE_DIR_PATH = '/Users/xxxs/Documents/public_ids/'

def request_url():
    url_root = "http://search.neijiang.gov.cn/?ty=&w=false&f=&rt=&adv=&dr=true&p=1&order=datetime&rp=&pos=-1&advtime=1&noteq=&adeq=&advrange=0&fq=&page=1&dept=&kw=%E5%90%8D%E5%8D%95%E5%85%AC%E7%A4%BA&czfs=2"

    url = 'http://zjj.neijiang.gov.cn/2018/10/3777005.html'
    url = "http://www.neijiang.gov.cn/zwgk/show/20180816102449-339497-00-000"
    url = "http://fgw.neijiang.gov.cn/2018/07/3514383.html"
    url = "http://www.neijiang.gov.cn/zwgk/show/20180824160614-225151-00-000"
    url = "http://zjj.neijiang.gov.cn/2018/08/3619546.html"
    url = "http://www.neijiang.gov.cn/zwgk/show/20180912152309-889907-00-000"
    url = "http://www.neijiang.gov.cn/zwgk/show/20180930100918-683595-00-000"
    url = "http://www.neijiang.gov.cn/zwgk/show/20181012101855-560834-00-000"
    url = "http://www.neijiang.gov.cn/zwgk/show/20181012101531-521214-00-000"


    headers = {  # 请求头请求刷新验证码和发送post时需要使用
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate'
    }

    print("get_area_zip_code stat...")
    session = requests.Session()
    print("get-url-is:", url)

    res = session.get(url, headers=headers)

    # 设置编码
    data = res.content.decode("utf-8", "ignore")
    soup_parse(url, data)


def soup_parse(url, content):
    soup = BeautifulSoup(content, "html.parser")

    for link in soup.findAll('a', attrs={'href': re.compile("^http://.*doc|docx|xls|xlsx|pdf")}):
        link_url = link['href']
        fix_url = link_url

        if (urlparse(link_url)[0] == "" and urlparse(link_url)[1] == ""):
            fix_url = urlparse(url)[0] + "://" + urlparse(url)[1] + "/" + link_url

        print("this_link_is=" + fix_url)
        download(link, fix_url)


def download(link, url):
    text = link.text
    open(SAVE_DIR_PATH + text + url[url.rfind('/') + 1:], 'wb').write(requests.get(url).content)


if __name__ == '__main__':
    print("-------------------")
    request_url()
