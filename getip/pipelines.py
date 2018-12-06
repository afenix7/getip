# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from bs4 import BeautifulSoup
import urllib
import requests
import socket
import traceback
import sys
import lxml

"""
作者：木马音响积木
链接：https://www.jianshu.com/p/c481feaf44fb
來源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
"""


class GetipPipeline(object):
    # validate_url = "http://ip.chinaz.com/getip.aspx"
    validate_url = "http://www.baidu.com"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 '
                      'Safari/537.36',
        'Accept-Language': 'zh-cn, zh;q=0.9,en;q=0.8;*,q=0.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    def __init__(self):
        self.file = open("iplist.txt", "a")
        self.sfile = open("siplist.txt", "a")

    def process_ip(self, ip_type, host, port):
        return 'https://' + host + ':' + port if ip_type == 'HTTPS' else 'http://' + host + ':' + port

    def validate_ip(self, proxy):
        try:
            # socket.setdefaulttimeout(3)
            proxy_temp = {"http": proxy}
            wb_data = requests.get(self.validate_url, headers=self.headers, proxies=proxy_temp)
            # print(proxy)
            print(wb_data)
            # soup = BeautifulSoup(wb_data.text, 'lxml')
            # print(soup)
            return True
        except:
            return False

    def write_ip(self, ip_type, item_string):
        try:
            if ip_type == 'HTTPS':
                self.sfile.write(item_string)
                self.sfile.write('\n')
            else:
                self.file.write(item_string)
                self.file.write('\n')
            print("增加add IP: " + item_string)
        except:
            print('file error 写入文件时发生错误')

    def process_item(self, item, spider):
        if '天' in str(item['time']):
            item_string = self.process_ip(str(item['type']), str(item['host']), str(item['port']))
            if self.validate_ip(item_string):
                self.write_ip(str(item['type']), item_string)
            else:
                print("\033[0;31m验证失败ip invalid: %s\033[0m" % item_string)
            return item
        else:
            raise DropItem('drop item: %s' % item)

    def close_spider(self, spider):
        self.file.close()
        self.sfile.close()
