# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from stores.items import StoresItem

class TaylormadeSpider(scrapy.Spider):
    name = "taylormade"
    allowed_domains = ['taylormadegolf.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                postal_code = row[1]
                latitude = row[9]
                longitude = row[10]
                url = "http://www.taylormadegolf.com/on/demandware.store/Sites-TMaG-Site/default/Stores-GetNearestStores?latitude=%s&longitude=%s&brand=taylormade&postalCode=%s&countryCode=US&distanceUnit=mi&maxdistance=52" % (latitude, longitude, postal_code)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []

        try:
            jsonresponse = json.loads(response.text)
            for row in jsonresponse["stores"]:
                item = StoresItem()
                item['name'] = row['name']
                item['address'] = "%s %s, %s %s %s %s" % (row['address1'], row['address2'], row['city'], row['stateCode'], row['postalCode'], row['countryCode'])
                item['phone'] = row['phone']
                item['website'] = row['storeWebsite']
                item['email'] = row['storeEmailAddress']
                item['hours_operation'] = row['storeHours']

                items.append(item)
        except:
            pass
        return items

