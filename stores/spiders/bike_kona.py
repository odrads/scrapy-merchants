# -*- coding: utf-8 -*-
import csv
import json
import scrapy
import re

from scrapy.http import FormRequest, Request

from stores.items import StoresItem

TAG_RE = re.compile(r'<[^>]+>')
MARKERS_RE = re.compile("var MyMarkers =  new Array\((.*)\)")

class BikeKonaSpider(scrapy.Spider):
    name = 'kona'
    start_urls = ['http://www.bullseyelocations.com/pages/KONATEST?f=1']
    download_delay = 1.5

    def parse(self, response):
        with open('./USPostalCode.txt', 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                address = "%s, %s" % (row[2], row[3])
                address = "NJ"
                EVENTVALIDATION = response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
                VIEWSTATE = response.css('input#__VIEWSTATE::attr(value)').extract_first()

                yield FormRequest(
                    'https://www.bullseyelocations.com/pages/KONATEST?f=1',
                    formdata = {
                        'ctl00$ToolkitScriptManager1': 'ctl00$ContentPlaceHolder1$upLocator|ctl00$ContentPlaceHolder1$searchButton',
                        '_TSM_HiddenField_': 'ypwUc8yhdocADBxkAn-jA4yOIU5A6IKiHhspMPKV3GA1',
                        'ctl00$ContentPlaceHolder1$hfKeywordTerm': '',
                        'ctl00$ContentPlaceHolder1$hfLocation': '',
                        'ctl00$ContentPlaceHolder1$hfOrigCoords': '',
                        'ctl00$ContentPlaceHolder1$hfNext': 'Next',
                        'ctl00$ContentPlaceHolder1$hfPrev': 'Prev',
                        'ctl00$ContentPlaceHolder1$hfMobile': 'false',
                        'ctl00$ContentPlaceHolder1$hfMobileDevice': '',
                        'ctl00$ContentPlaceHolder1$hfLocationTerm': 'City & State OR Zip Code',
                        'ctl00$ContentPlaceHolder1$hfCountry': 'United States',
                        'ctl00$ContentPlaceHolder1$countryList': '1',
                        'ctl00$ContentPlaceHolder1$hfResultsPerPage': '5',
                        'ctl00$ContentPlaceHolder1$radiusList': '50',
                        'ctl00$ContentPlaceHolder1$txtCityStateZip': address,
                        '__VIEWSTATEGENERATOR': '86D50429',
                        '__LASTFOCUS': '',
                        '__EVENTTARGET': '',
                        '__EVENTARGUMENT': '',
                        '__VIEWSTATE': VIEWSTATE, 
                        '__EVENTVALIDATION': EVENTVALIDATION,
                        'ctl00$ContentPlaceHolder1$searchButton': 'Search'
                    }, 
                    callback = self.parse_item
                )
                break
                

    def parse_item(self, response):
        print(response.body)
        # jsonresponse = MARKERS_RE.search(response.body)
        # print(jsonresponse)
        # items = []
        # if jsonresponse:
        #     try:
        #         data_str = jsonresponse.group(1).replace("'", '"')

        #         seeds = 'name','address','lat','lon','id','origindex','dirlink','url','email','linkColor','region','web','locImage','couponText','couponLink','couponThumb','GeoCodeStatusId','type','detailsLink','eventLink','mapIcon','locationTypeName','mobileNumber','phoneNumber'
        #         for seed in seeds: 
        #             data_str = data_str.replace('%s:' % seed, '"%s":' % seed)
        #         data_str = "[%s]" % data_str

        #         rows = json.loads(data_str)
        #         for row in rows:
        #             item = StoresItem()
        #             item['name'] = TAG_RE.sub('', row['name'])
        #             item['address'] = TAG_RE.sub('', "%s %s" % (row['address'], row['region']))
        #             item['phone'] = row['phoneNumber']
        #             item['website'] = row['url']
        #             item['email'] = row['email']
        #             item['hours_operation'] = ''

        #             items.append(item)
        #     except Exception as e:
        #         pass
        # return items


