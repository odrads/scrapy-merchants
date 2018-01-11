# -*- coding: utf-8 -*-
import csv
import scrapy

from scrapy.selector import Selector

from stores.items import StoresItem

class WatchTagheuerSpider(scrapy.Spider):
    name = "tagheuer"
    allowed_domains = ['tagheuer.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                address = "%s %s United States" % (row[2], row[3])
                url = "https://store.tagheuer.com/search?query=%s" % (address)
                request = scrapy.Request(url=url, callback=self.parse)
                request.meta['address'] = address
                yield request

    def parse(self, response):
        sel = Selector(response)
        pages = len(sel.xpath("//li[@class='components-navigation-pagination-basic__pages__page']/text()").extract())
        address = response.meta['address']
        if pages > 0:
            for page in xrange(pages):
                p = page + 1
                url = "https://store.tagheuer.com/search?query=%s&page=%d" % (address, p)
                request = scrapy.Request(url=url, callback=self.parse_item)
                yield request
        else:
            url = "https://store.tagheuer.com/search?query=%s&page=1" % (address)
            request = scrapy.Request(url=url, callback=self.parse_item)
            yield request

    def parse_item(self, response):
        sel = Selector(response)
        items = []

        stores = sel.xpath("//div[@class='components-outlet-item-search-result-basic__link__details']")
        for row in stores:
            item = StoresItem()
            name = row.xpath(".//a/h3/span/text()").extract()
            if len(name)>0:
                item['name'] = name[0].strip()
            else:
                item['name'] = ''

            address1 = row.xpath("normalize-space(.//address[@class='components-outlet-item-address-basic components-outlet-item-search-result-basic__link__details__access__address'])").extract()
            if len(address1)>0:
                item['address'] = address1[0]
            else:
                item['address'] = ''
            
            phone = row.xpath("normalize-space(.//span[@class='components-outlet-item-phone-basic__phone__number'])").extract()
            if len(phone)>0:
                item['phone'] = phone[0]
            else:
                item['phone'] = ''
            item['website'] = ''
            item['email'] = ''
            item['hours_operation'] = ''

            items.append(item)
        return items
   

