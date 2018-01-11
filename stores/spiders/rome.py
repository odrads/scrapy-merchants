# -*- coding: utf-8 -*-
import csv
import scrapy

from stores.items import StoresItem


class SnowboardRomeSpider(scrapy.Spider):
    name = 'rome'
    allowed_domains = ['romesnowboards.com']
    start_urls = ["http://www.romesnowboards.com/shops/"]

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                postal_code = row[1]
                # postal_code = '94501'
                url = "http://www.romesnowboards.com/shops/"
                formdata = {'zipcode': postal_code}
                yield scrapy.FormRequest(url,
                     formdata=formdata,
                     callback=self.parse)
                # break

    def parse(self, response):
        sel = scrapy.Selector(response)
        items = []

        stores = sel.xpath('//div[@id="shop-list"]/p')
        for row in stores:
            item = StoresItem()
            name = row.xpath("../h4/text()").extract()
            if len(name)>0:
                item['name'] = name[0].strip()
            else:
                item['name'] = ''

            item['address'] = ''
            item['phone'] = ''
            address1 = row.xpath("./text()").extract()

            if len(address1)>0:
                item['address'] = (address1[0] + address1[1]).replace('\n', '').strip(' ')
                item['phone'] = address1[2].replace('\n', '').replace('Tel:', '').strip(' ')
            
            item['website'] = ''
            item['email'] = ''
            item['hours_operation'] = ''

            items.append(item)
        return items


