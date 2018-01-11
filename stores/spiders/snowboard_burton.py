# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from stores.items import StoresItem

class SnowboardBurtonSpider(scrapy.Spider):
    name = "burton"
    allowed_domains = ['burton.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                latitude = row[9]
                longitude = row[10]
                url = 'https://www.burton.com/on/demandware.store/Sites-Burton_NA-Site/en_US/Stores-FetchStoresJSON?radius=100&latitude=%s&longitude=%s' % (latitude, longitude)
                yield scrapy.Request(url=url, callback=self.parse)
                
    def parse(self, response):
        items = []
        try:
            jsonresponse = json.loads(response.text)
            for row in jsonresponse:
                item = StoresItem()
                item['name'] = ' ' . join(row['dealerTypes'])
                item['address'] = "%s %s %s %s %s" % (row['address'], row['city'], row['state'], row['postalCode'], row['countryCD'])
                item['phone'] = row['telephone'].replace('tel:', '')
                item['website'] = ''
                item['email'] = ''
                item['hours_operation'] = ''

                items.append(item)
        except:
            pass
        return items

