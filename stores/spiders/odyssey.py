# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from stores.items import StoresItem

class OdysseySpider(scrapy.Spider):
    name = "odyssey"
    allowed_domains = ['odysseygolf.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                postal_code = row[1]
                latitude = row[9]
                longitude = row[10]
                address = "%s %s" % (row[2], row[3])
                url = "http://www.odysseygolf.com/on/demandware.store/Sites-ODY2-Site/default/Stores-GetLocations?address=%s&country=US&distanceKm=160.93&services=31" % (address)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
        try:
            jsonresponse = json.loads(response.text)
            if "StatusCode" in jsonresponse:
                for row in jsonresponse["ResponseContainer"]["RetailLocations"]:
                    item = StoresItem()
                    item['name'] = row['Name']
                    item['address'] = "%s %s, %s %s %s %s" % (row['Street1'], row['Street2'], row['City'], row['RegionCode'], row['PostalCode'], row['Country'])
                    item['phone'] = row['Phone']
                    item['website'] = ''
                    item['email'] = ''
                    item['hours_operation'] = ''

                    items.append(item)
        except:
            pass
        return items

