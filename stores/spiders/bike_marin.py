# -*- coding: utf-8 -*-
import csv
import json
import scrapy
import pprint
import re

from scrapy.selector import Selector

from stores.items import StoresItem

SEARCHPAGE_RE = re.compile('searchPageData":(.*)')

class BikeMarinSpider(scrapy.Spider):
    name = "marin"
    allowed_domains = ['marinbikes.com']
    download_delay = 1.5

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                postal_code = row[1]
                # postal_code = '99654'
                url = "https://www.marinbikes.com/find-a-dealer?near=%s" % postal_code
                yield scrapy.Request(url=url, callback=self.parse)
                # break

    def parse(self, response):  
        sel = Selector(response)
        stores = sel.xpath("//div[@class='locator__result']")
        items = []

        for row in stores:
            item = StoresItem()
            name = row.xpath("h2/text()").extract()[0]
            item['name'] = name

            addr = []
            addrs_path = row.xpath('div[@class="locator__result-content"]/text()').extract()
            for a in addrs_path:
                if a.strip():
                    addr.append(a.strip())
            address = ' ' . join(addr)
            item['address'] = address

            website = row.xpath('div[@class="locator__result-content"]/a[contains(., "Website")]/@href').extract()
            if website:
                website = website[0].strip()
            item['website'] = website

            phone = row.xpath('div[@class="locator__result-content"]/a[contains(@href, "tel:")]/text()').extract()
            if phone:
                phone = phone[0].strip()
            item['phone'] = phone
            item['email'] = ''
            item['hours_operation'] = ''

            items.append(item)
        return items

            
