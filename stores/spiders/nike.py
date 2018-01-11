# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from scrapy.selector import Selector

from stores.items import StoresItem


class NikeSpider(scrapy.Spider):
    name = 'nike'
    allowed_domains = ['nike.com']
    start_urls = ["https://www.nike.com/us/en_us/retail/en/directory"]
    download_delay = 1.5

    # url = "https://www.ping.com/locator/GetRetailersInLatLongBounds"

    def parse(self, response):
        sel = Selector(response)

        rows = sel.xpath('//div[@class="bwt-directory-store-wrapper bwt-hide-on-mobile"]')
        for row in rows:
            url = 'https://www.nike.com%s' % row.xpath('a/@href').extract_first()
            name = row.xpath('./a/div[@class="bwt-store-city-wrapper"]/text()').extract_first()
            address = ' '.join(row.xpath('./a/div[@class="bwt-store-address-wrapper"]//div[@class="bwt-store-address-line"]/text()').extract()).replace('\n', '')
            
            request = scrapy.Request(url=url, callback=self.parse_item)
            request.meta['name'] = name
            request.meta['address'] = address
            yield request


    def parse_item(self, response):
        sel = Selector(response)
        name = response.meta['name']
        address = response.meta['address']
        website = response.url
        items = []

        item = StoresItem()
        item['name'] = name
        item['address'] = address
        item['website'] = website
        item['phone'] = sel.xpath('//span[@class="bwt-store-phone-number-link-text"]/text()').extract_first().replace('\n', '')
        item['hours_operation'] = ' ' . join(sel.xpath('//div[@class="bwt-store-hours-range"]/text()').extract()).replace('\n', '')
        item['email'] = ''
        items.append(item)
        
        return items
