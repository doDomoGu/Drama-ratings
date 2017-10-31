''' module scrapy  '''
import scrapy

import sys

import pymysql.cursors

class listpageSpider(scrapy.Spider):
    
    ''' HideystudioSpider '''
    name = 'list_page'

    custom_settings = {
        'ITEM_PIPELINES': {
            'ys.pipelines_list.ListPipeline': 300,
        }
    }

    connection = pymysql.connect(
        host='localhost',
        user='gljgljglj',
        password='gljgogo',
        db='ys',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    select_sql = "select * from `page` " #+ " where year = '2009' and season = '1'" 

    cursor = connection.cursor()
    cursor.execute(select_sql)

    pages = cursor.fetchall()



    allowed_domains = ['hideystudio.com']
    start_urls = []
        
    for page in pages:

        start_urls.append('http://www.hideystudio.com/rank/'+page['url'])


    ''' 
    localMode = True

    if localMode:
        allowed_domains = ['localhost']
        start_urls = [
            'http://localhost/python/tutorial/ys/result/rank.html',
        ]
    else:
        allowed_domains = ['hideystudio.com']
        start_urls = [
            'http://www.hideystudio.com/rank/index.html'
        ] '''

    def parse(self, response):

        print( response.url)
        filename = response.url.split("/")[-1]
        print(filename)

        open('ys/rank/'+filename, 'wb').write(response.body)  
        
