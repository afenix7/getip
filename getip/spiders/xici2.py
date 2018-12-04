# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from getip.items import GetipItem


class Xici2Spider(CrawlSpider):
    name = 'xici2'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn']

    rules = (
        # 分页
        Rule(LinkExtractor(allow=r'http://www.xicidaili.com/nn/\d+/$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 参考 https://www.cnblogs.com/qlshine/p/5926103.html
        table = response.xpath('//table[@id="ip_list"]')[0]
        trs = table.xpath('//tr')[1:]  # 去掉标题行
        items = []
        for tr in trs:
            pre_item = GetipItem()
            pre_item['host'] = tr.xpath('td[2]/text()').extract()[0]
            pre_item['port'] = tr.xpath('td[3]/text()').extract()[0]
            pre_item['type'] = tr.xpath('td[6]/text()').extract()[0]
            pre_item['time'] = tr.xpath('td[9]/text()').extract()[0]
            items.append(pre_item)
        return items