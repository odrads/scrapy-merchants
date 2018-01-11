# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from stores.items import StoresItem

class DCSpider(scrapy.Spider):
    name = "dc"
    allowed_domains = ['dcshoes.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                latitude = row[9]
                longitude = row[10]
                url = "http://www.dcshoes.com/on/demandware.store/Sites-DC-US-Site/en_US/StoreLocator-StoreLookup?latitude=%s&longitude=%s&mapRadius=30" % (latitude, longitude)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []

        try:
            jsonresponse = json.loads(response.text)
            print(jsonresponse)
            if "stores" in jsonresponse:
                for row in jsonresponse["stores"]:
                    item = StoresItem()
                    item['name'] = row['name']
                    item['address'] = "%s %s %s US" % (row['address'], row['city'], row['postalCode'])
                    item['phone'] = row['phone']
                    item['website'] = ''
                    item['email'] = ''
                    item['hours_operation'] = ''

                    items.append(item)
        except:
            pass
        return items

