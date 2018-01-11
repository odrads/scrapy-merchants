# -*- coding: utf-8 -*-
import csv
import json
import scrapy
from scrapy.selector import Selector

from stores.items import StoresItem

class SnowboardGNUSpider(scrapy.Spider):
    name = "gnu"
    allowed_domains = ['locally.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                location = row[2] + ' ' + row[3]
                url = 'https://gnu.locally.com/in/%s' % location
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        sections = sel.xpath("//section[@id='landing-page-locations']//div[@class='horizontal-scroll-container']/a")
        for section in sections:
            href = section.xpath("@href").extract()[0]
            url = 'https://libtechsnow.locally.com%s' % href
            request = scrapy.Request(url=url, callback=self.parse_item)
            yield request

    def parse_item(self, response):
        sel = Selector(response)
        item = StoresItem()

        name = sel.xpath('//h1[contains(@class, "brand-retail-title")]/text()').extract()
        if len(name)>0:
            item['name'] = name[0].strip()
        else:
            item['name'] = ''

        item['address'] = ''
        item['phone'] = ''
        address1 = sel.xpath("//div[contains(@class, 'landing-header-detail-section')]/text()").extract()
        if len(address1)>0:
            item['address'] = address1[0].replace('\n', '').strip() + ' ' + address1[1].replace('\n', '').strip()
            item['phone'] = address1[2].replace('\n', '').strip()

        item['website'] = ''
        item['email'] = ''
        item['hours_operation'] = ''

        return item
