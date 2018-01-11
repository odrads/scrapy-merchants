# -*- coding: utf-8 -*-
import csv
import scrapy
import json

from scrapy.selector import Selector

from stores.items import StoresItem

class WatchSeikoSpider(scrapy.Spider):
    name = "seiko"
    allowed_domains = ['seikowatches.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                latitude = row[9]
                longitude = row[10]
                url = "https://store-api.seikowatches.com/stores/tile?format=json&lat=%s&lng=%s&range=0.5&lang=en" % (latitude, longitude)
                request = scrapy.Request(url=url, callback=self.parse)
                yield request

    def parse(self, response):
        jsonresponse = json.loads(response.text)
        if 'stores' in jsonresponse:
            stores = jsonresponse['stores']
            for store in stores:
                name = store['name_translations'][0]['content']
                city = store['city']['translations'][0]['content']
                address = store['address_translations'][0]['content']
                print(name, address, city)
                # print(store['name_translations'][0]['content'], store['city'][0]['translations'][0]['content'], store['address_translations'][0]['content'])
