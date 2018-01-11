# -*- coding: utf-8 -*-
import csv
import json
import scrapy
import pprint
import re

from stores.items import StoresItem

SEARCHPAGE_RE = re.compile('searchPageData":(.*)')

class BikeTrekSpider(scrapy.Spider):
    name = "trek"
    allowed_domains = ['trekbikes.com']
    download_delay = 1.5

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                address = "%s, %s, United States" % (row[2], row[3])
                # address = "Los Angeles California"
                url = "https://www.trekbikes.com/us/en_US/store-finder/json/?q=%s&sort=Distance&distance=500" % (address)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if 'searchPageData' in response.body:
            # print(response.body)
            if 'numberPagesShown' in response.body:
                numberPagesShown = 0
                try:
                    jsonresponse = json.loads(response.text)
                    numberPagesShown = int(jsonresponse['numberPagesShown'])
                except ValueError as error:
                    pass
                if numberPagesShown > 0:
                    for page in range(numberPagesShown):
                        url = "%s&page=%d" % (response.url, page)
                        yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        items = []

        jsonresponse = json.loads(response.body)
        for row in jsonresponse['searchPageData']['results']:
            item = StoresItem()
            item['name'] = row['displayName']
            item['address'] = row['address']['formattedAddress']
            item['phone'] = row['address']['phone']
            item['website'] = "https://www.trekbikes.com/us/en_US/%s" % row['url']

            item['email'] = row['address']['email']
            hours_operation = ''
            if 'openingHours' in row:
                try:
                    for sched in row['openingHours']['weekDayOpeningList']:
                        if sched['storeOpeningTime']:
                            hours_operation += "%s: %s - %s;" % (sched['weekDay'], sched['storeOpeningTime']['formattedHour'], sched['storeClosingTime']['formattedHour'])
                except:
                    pass
            item['hours_operation'] = hours_operation

            items.append(item)

        return items
