# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from stores.items import StoresItem

class BikeScottSpider(scrapy.Spider):
    name = "scott"
    allowed_domains = ['scott-sports.com']

    def start_requests(self):
        urls = []
        with open('../country.csv', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                address = "%s, %s" % (row[2], row[3])
                params = '{"address":"%s","countryIsocode":"US","country":false,"radius":321.868,"division":"bike"}' % (address)
                url = "https://www.scott-sports.com/us/en/dealers/locator/getDealers?query=%s" % (params)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []

        try:
            jsonresponse = json.loads(response.text)
            for row in jsonresponse['dealers']:
                item = StoresItem()
                item['name'] = row['dealerName']
                item['address'] = "%s %s %s %s %s" % (row['streetName'], row['district'], row['town'], row['postalCode'], row['countryName'])
                item['phone'] = row['phone']
                item['website'] = row['homePageUrl']
                item['email'] = row['email']
                item['hours_operation'] = ''

                items.append(item)
        except:
            pass
        return items

