# -*- coding: utf-8 -*-
import csv
import json
import scrapy
import re

from scrapy.http import FormRequest, Request

from stores.items import StoresItem

TAG_RE = re.compile(r'<[^>]+>')
MARKERS_RE = re.compile("var MyMarkers =  new Array\((.*)\)")

class MizunoSpider(scrapy.Spider):
    name = 'mizuno'
    start_urls = ['https://mizuno.bullseyelocations.com/general?f=1&category=Golf']
    download_delay = 1.5

    def parse(self, response):
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                address = "%s, %s" % (row[2], row[3])
                EVENTVALIDATION = response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
                VIEWSTATE = response.css('input#__VIEWSTATE::attr(value)').extract_first()
                yield FormRequest(
                    'https://mizuno.bullseyelocations.com/general?f=1&category=Golf',
                    headers = {'user-agent': 'Mozilla/5.0'},
                    formdata = {
                        'ctl00$ToolkitScriptManager1': 'ctl00$ContentPlaceHolder1$upLocator|ctl00$ContentPlaceHolder1$searchButton',
                        '_TSM_HiddenField_': 'ypwUc8yhdocADBxkAn-jA4yOIU5A6IKiHhspMPKV3GA1',
                        'ctl00$ContentPlaceHolder1$hfKeywordTerm': '',
                        'ctl00$ContentPlaceHolder1$hfLocation': '',
                        'ctl00$ContentPlaceHolder1$hfOrigCoords': '',
                        'ctl00$ContentPlaceHolder1$hfMobile': 'false',
                        'ctl00$ContentPlaceHolder1$hfMobileDevice': '',
                        'ctl00$ContentPlaceHolder1$hfCountry': 'United States',
                        'ctl00$ContentPlaceHolder1$hfSearch': '',
                        'ctl00$ContentPlaceHolder1$countryList': '1',
                        'ctl00$ContentPlaceHolder1$tweLocation_ClientState': '', 
                        'ctl00$ContentPlaceHolder1$txtKeyword': '',
                        'ctl00$ContentPlaceHolder1$tweKeyword_ClientState': '',
                        'ctl00$ContentPlaceHolder1$ddlCategories': '-1',
                        'ctl00$ContentPlaceHolder1$hfTotalPages': '',
                        'ctl00$ContentPlaceHolder1$hfResultsPerPage': '10000',
                        'ctl00$ContentPlaceHolder1$radiusList': '100',
                        'ctl00$ContentPlaceHolder1$txtCityStateZip': address,
                        'ctl00$ContentPlaceHolder1$chklistCat$1': '85266',
                        '__LASTFOCUS': '',
                        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$countryList',
                        '__VIEWSTATE': VIEWSTATE, 
                        '__EVENTVALIDATION': EVENTVALIDATION,
                        'ctl00$ContentPlaceHolder1$searchButton': 'Search'
                    }, 
                    callback = self.parse_item
                )
                

    def parse_item(self, response):
        jsonresponse = MARKERS_RE.search(response.body)

        items = []
        if jsonresponse:
            try:
                data_str = jsonresponse.group(1).replace("'", '"')

                seeds = 'name','address','lat','lon','id','origindex','dirlink','url','email','linkColor','region','web','locImage','couponText','couponLink','couponThumb','GeoCodeStatusId','type','detailsLink','eventLink','mapIcon','locationTypeName','mobileNumber','phoneNumber'
                for seed in seeds: 
                    data_str = data_str.replace('%s:' % seed, '"%s":' % seed)
                data_str = "[%s]" % data_str

                rows = json.loads(data_str)
                for row in rows:
                    item = StoresItem()
                    item['name'] = TAG_RE.sub(' ', row['name'])
                    item['address'] = TAG_RE.sub(' ', "%s %s" % (row['address'], row['region']))
                    item['phone'] = row['phoneNumber']
                    item['website'] = row['url']
                    item['email'] = row['email']
                    item['hours_operation'] = ''

                    items.append(item)
            except Exception as e:
                pass
        return items


