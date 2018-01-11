# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from collections import OrderedDict


class StoresItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    hours_operation = scrapy.Field()

    def keys(self):
        return ['name', 'address', 'website', 'phone', 'email', 'hours_operation']
