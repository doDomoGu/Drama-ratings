''' module scrapy  '''
import scrapy

import sys

import pymysql.cursors

import re

import configparser

from ys.items import PageItem

class listSpider(scrapy.Spider):
    
    conf = configparser.ConfigParser()
    conf.read('ys/conf.ini')

    ''' HideystudioSpider '''
    name = 'list'

    custom_settings = {
        'ITEM_PIPELINES': {
            'ys.pipelines_list.ListPipeline': 300,
        }
    }

    connection = pymysql.connect(
        host = conf.get('MYSQL', 'host'),
        user = conf.get('MYSQL', 'user'),
        password = conf.get('MYSQL', 'password'),
        db = conf.get('MYSQL', 'db'),
        charset = 'utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    update_sql = "update `page` set `status` = 0"

    connection.cursor().execute(update_sql)

    connection.commit()

    localMode = conf.getboolean('SETTING', 'localmode')

    if localMode:
        allowed_domains = ['localhost']
        start_urls = [
            'http://localhost/python/tutorial/ys/rank/index.html',
        ]
    else:
        allowed_domains = ['hideystudio.com']
        start_urls = [
            'http://www.hideystudio.com/rank/index.html'
        ]

    def parse(self, response):

        season_arr  = {1:'winter',2:'spring',3:'summer',4:'autumn'}
        season_arr2 = {'winter':1,'spring':2,'summer':3,'autumn':4}

        ul_all = response.css('.dropdown_4columns').xpath('.//div[@class="col_1"]/ul')
        
        if len(ul_all) == 4:
            i = 1
            for ul_one in ul_all:
                season = season_arr[i]
                season_id = i
                a_all = ul_one.xpath('./li/a')

                for a_one in a_all:
                    url = a_one.xpath('@href').extract_first()
                    #print(type(a_one.xpath('text()').extract_first()))

                    y = a_one.xpath('text()').extract_first()
                    year = re.sub('[^0-9]','',y)

                    print(url,'/',year,'/',season)



                    page_item = PageItem()
                    page_item['url'] =  url
                    page_item['year'] = year
                    page_item['season'] = i #season

                    
                    yield page_item


                i += 1

        else:
            # 列表获取失败
            pass
        return True
