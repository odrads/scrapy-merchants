# -*- coding: utf-8 -*-
import csv
import json
import scrapy
import pprint
import re

from scrapy.selector import Selector
from scrapy.http import FormRequest  

from stores.items import StoresItem

SEARCHPAGE_RE = re.compile('searchPageData":(.*)')

class BikeGTSpider(scrapy.Spider):
    name = "gt"
    allowed_domains = ['gtbicycles.com']
    download_delay = 1.5
    start_urls = ['http://dealerlocator.gtbicycles.com/']

    # def start_requests(self):
    #     urls = []
    #     with open('./USPostalCode.txt', 'r') as f:
    #         reader = csv.reader(f, delimiter='\t')
    #         for row in reader:
    #             postal_code = row[1]
    #             # postal_code = '95117'
    #             yield FormRequest.from_response(response,
    #                                     formname="store_locator_form",
    #                                     formdata={"address": 'San Francisco United States'},
    #                                     callback=self.parse)
    #             break

    def parse(self, response):  
        yield FormRequest.from_response(response=response,
            formdata={"address": 'San Francisco United States'},
            callback=self.parse_item)

    def parse_item(self, response):
        print(response.body)
    
            
