# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from stores.items import StoresItem

class BikeMeridaSpider(scrapy.Spider):
    name = "merida"
    allowed_domains = ['merida-bikes.com']

    def start_requests(self):
        urls = []
        with open('../country.csv', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                latitude = row[1]
                longitude = row[2]
                url = "https://www.merida-bikes.com/dealer/markers?lat=%s&lng=%s" % (latitude, longitude)
                yield scrapy.Request(url=url, callback=self.parse)
          
    def parse(self, response):
        items = []

        try:
            jsonresponse = json.loads(response.text)
            for row in jsonresponse:
            	item = StoresItem()
                item['name'] = "%s %s" % (jsonresponse[row]['name'], jsonresponse[row]['name2'])
                item['address'] = "%s %s %s %s" % (jsonresponse[row]['street'], jsonresponse[row]['town'], jsonresponse[row]['zip'], jsonresponse[row]['country'])
                item['phone'] = jsonresponse[row]['phone']
                item['website'] = jsonresponse[row]['url']
                item['email'] = jsonresponse[row]['email']
                item['hours_operation'] = ''

                items.append(item)
        except:
            pass
        return items

