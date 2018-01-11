# -*- coding: utf-8 -*-
import csv
import json
import scrapy
import pprint
import re

from stores.items import StoresItem

class SnowboardSalomonSpider(scrapy.Spider):
    name = "salomon"
    allowed_domains = ['salomon.com']
    start_urls = [
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=United+States'
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Austria',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Canada',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=China',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Czech Republic',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Denmark',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Finland',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=France',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Germany',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Italy',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Japan',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Mexico',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Netherlands',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Norway',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Poland',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Russia',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Spain',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Sweden',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=Switzerland',
        'https://www.salomon.com/us/store/get-brandstores.json?page=1&country=United States',
        ]

    def parse(self, response):
        items = []

        try:
            jsonresponse = json.loads(response.text)
            for row in jsonresponse['brandstores']:
                item = StoresItem()
                item['name'] = row['name'].replace('\r', '').replace('<br/>', ' ').replace('<br />', ' ')
                item['address'] = row['address'].replace('\r', '').replace('<br/>', ' ').replace('<br />', ' ')
                item['address'] = ("%s %s %s %s" % (row['address'], row['city'], row['postal_code'], row['country'])).replace('\r', '').replace('<br/>', ' ').replace('<br />', ' ')
                item['phone'] = row['telephone']
                item['website'] = ''
                item['email'] = row['email'].replace('\r', '').replace('<br/>', ' ').replace('<br />', ' ')
                item['hours_operation'] = row['hours'].replace('\r', '').replace('<br/>', ' ').replace('<br />', ' ')

                items.append(item)
        except:
            pass
        return items
