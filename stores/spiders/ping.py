# -*- coding: utf-8 -*-
import csv
import json
import scrapy
from scrapy.http import FormRequest  

from stores.items import StoresItem


class PingSpider(scrapy.Spider):
    name = 'ping'
    allowed_domains = ['ping.com']
    start_urls = ["ping.com"]

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                latitude = row[9]
                longitude = row[10]
                url = "https://ping.com/FindRetailerAPI?Lat=%s&Long=%s&Radius=100" % (latitude, longitude)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
        try:
            jsonresponse = json.loads(response.text)
            if "Retailers" in jsonresponse:
                i = 0
                for row in jsonresponse['Retailers']:
                    item = StoresItem()
                    item['name'] = row['Name']
                    item['address'] = "%s %s" % (row['Address1'], row['Address2'])
                    item['phone'] = row['Phone']
                    item['website'] = row['Website']
                    item['email'] = ''
                    item['hours_operation'] = ''

                    items.append(item)
        except:
            pass
        return items


