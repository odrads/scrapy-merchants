# -*- coding: utf-8 -*-
import csv
import scrapy

from scrapy.selector import Selector

from stores.items import StoresItem

class SnowboardRideSpider(scrapy.Spider):
    name = "ride"
    allowed_domains = ['ridesnowboards.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                postal_code = row[1]
                latitude = row[9]
                longitude = row[10]
                latitude = '37.7848'
                longitude = '-122.7278'
                # https://www.ridesnowboards.com/on/demandware.store/Sites-Ride_Snowboards_US-Site/en_US/
                url = "https://www.ridesnowboards.com/on/demandware.store/Sites-Ride_Snowboards_US/default/StoreLocator-StoreLookup?lat=%s&lng=%s&countryCode=US&postalCode=%s&mileRadius=99999&dService=&cProduct=" % (latitude, longitude, postal_code)
                yield scrapy.Request(url=url, callback=self.parse)
                break
 
    def parse(self, response):
        print(response.body)
        # sel = Selector(response)
        # stores = sel.xpath("//div[@class='store-address']")
        # items = []

        # for row in stores:
        #     item = StoresItem()
        #     name = row.xpath("div[@class='store-name']/text()").extract()
        #     if len(name)>0:
        #         item['name'] = name[0]
        #     else:
        #         item['name'] = ''

        #     address1 = row.xpath("div[2]/text()").extract()
        #     if len(address1)>0:
        #         item['address'] = address1[0]
        #     else:
        #         item['address'] = ''
        #     address2 =  row.xpath("div[4]/text()").extract()
        #     if len(address2)>0:
        #         item['address'] = item['address']  + ' ' + address2[0]

        #     address3 =  row.xpath("div[5]/text()").extract()
        #     if len(address3)>0:
        #         item['address'] = item['address']  + ' ' + address3[0]
            
        #     phone = row.xpath("div[6]/text()").extract()
        #     if len(phone)>0:
        #         item['phone'] = phone[0]
        #     else:
        #         item['phone'] = ''
        #     item['website'] = ''
        #     item['email'] = ''
        #     item['hours_operation'] = ''

        #     items.append(item)
        # return items
   

