# -*- coding: utf-8 -*-
import csv
import json
import scrapy
import pprint
import re

from stores.items import StoresItem

class BikeGiantSpider(scrapy.Spider):
    name = "giant"
    allowed_domains = ['giant-bicycles.com']
    download_delay = 1.5

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                try:
                    postal_code = row[1]
                    latitude = row[9]
                    longitude = row[10]
                    city = row[2] + " " + row[3]
                    url = "https://www.giant-bicycles.com/us/stores/dealers" 
                    payload = {"latitude": latitude,
                        "longitude": longitude,
                        "keyword": city,
                        "NE_lat":0,
                        "NE_lng":0,
                        "SW_lat":0,
                        "SW_lng":0,
                        "campaigncodes":[],
                        "onlyGiantStores": "false"}
                    yield scrapy.Request(url,
                        method='POST', 
                        body=json.dumps(payload), 
                        headers={'Content-Type':'application/json'})
                except Exception as err:
                    print(err)
                
               

    def parse(self, response):
        items = []

        try:
            jsonresponse = json.loads(response.text)
            for row in jsonresponse['dealers']:
                item = StoresItem()
                item['name'] = row['Name']
                item['address'] = row['AddressLocalized']
                item['phone'] = row['Phone']
                item['website'] = row['WebAddress']
                item['email'] = row['Email']
                item['hours_operation'] = ''

                items.append(item)
        except:
            pass
        return items
