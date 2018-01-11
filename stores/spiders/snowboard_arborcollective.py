# -*- coding: utf-8 -*-
import csv
import json
import scrapy

from stores.items import StoresItem

class SnowboardArborCollectiveSpider(scrapy.Spider):
    name = "arbor"
    allowed_domains = ['arborcollective.com']

    def start_requests(self):
        urls = []
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                postal_code = row[1]
                url = 'http://arborcollective.com/cms/wp-content/themes/arbor/ajax-get-dealers.php'
                formdata = {'location': postal_code}
                yield scrapy.FormRequest(url,
                     formdata=formdata,
                     callback=self.parse)

    def parse(self, response):
        items = []
        try:
            jsonresponse = json.loads(response.text)
            for row in jsonresponse:
                item = StoresItem()
                item['name'] = row['name']
                item['address'] = "%s %s %s %s %s US" % (row['address'], row['suburb'], row['city'], row['state'], row['zip'])
                item['phone'] = row['phone'].replace('tel:', '')
                item['website'] = row['website']
                item['email'] = ''
                item['hours_operation'] = ''

                items.append(item)
        except:
            pass
        return items

