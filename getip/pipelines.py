# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GetipPipeline(object):
    def process_item(self, item, spider):
        file = open("/proxy/list.txt", "a")
        item_string = str(item)
        file.write(item_string)
        file.write('\n')
        file.close()
        print(item_string)
        return item
