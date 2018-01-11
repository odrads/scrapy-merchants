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
                postal_code = row[1]
                latitude = row[9]
                longitude = row[10]
                address = "%s, %s, United States" % (row[2], row[3])
                url = "https://www.ping.com/locator/GetRetailersInLatLongBounds"
                formdata = {'address': address,
                            'radius': '100',
                            'type': 'dealers',
                            'latitude': '',
                            'longitude': ''}
                yield scrapy.FormRequest(url,
                     formdata=formdata,
                     callback=self.parse)

    def parse(self, response):
        items = []

        try:
            jsonresponse = json.loads(response.text)
            if "maps" in jsonresponse:
                for row in jsonresponse['maps']['items']:
                    item = StoresItem()
                    item['name'] = row['title']
                    item['address'] = "%s %s %s %s" % (row['street'], row['city'], row['postal_code'], row['country_id'])
                    item['phone'] = row['phone']
                    item['website'] = row['website']
                    item['email'] = ''
                    item['hours_operation'] = ''

                    items.append(item)
        except:
            pass
        return items


