# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class GetipPipeline(object):
    def __init__(self):
        self.file = open("list.txt", "a")

    def process_item(self, item, spider):
        if str(item['type']) == 'HTTP' and '天' in str(item['time']):
            item_string = 'http://' + str(item['host']) + ':' + str(item['port'])
            self.file.write(item_string)
            self.file.write('\n')
            print(item_string)
            return item
        else:
            raise DropItem('drop item: %s' % item)

    def close_spider(self, spider):
        self.file.close()
