# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from stores.items import StoresItem


class TitleistSpider(scrapy.Spider):
    name = 'titleist'
    allowed_domains = ['titleist.com']
    
    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                postal_code = row[1]
                latitude = row[9]
                longitude = row[10]
                url = "https://www.titleist.com/locator/ajax?latitude=%s&longitude=%s&radius=100" % (latitude, longitude)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
        try:
            jsonresponse = json.loads(response.text)
            for row in jsonresponse:
                item = StoresItem()
                item['name'] = row['label']
                item['address'] = "%s %s %s, %s %s %s" % (row['address1'], row['address2'], row['county'], row['city'], row['state'], row['zipcode'])
                item['phone'] = row['phone']
                item['website'] = row['website']
                item['email'] = row['email']
                item['hours_operation'] = row['hours']

                items.append(item)
        except:
            pass
        return items
