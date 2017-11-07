''' module scrapy  '''
import scrapy

import sys

import pymysql.cursors

import re

from ys.items import DramaItem, TvItem, TimeItem, AllItem

import configparser

class HideystudioSpider(scrapy.Spider):

    conf = configparser.ConfigParser()
    conf.read('ys/conf.ini')

    custom_settings = {
        'ITEM_PIPELINES': {
            'ys.pipelines.DramaPipeline': 300,
        }
    }

    ''' HideystudioSpider '''
    name = 'ys'

    connection = pymysql.connect(
        host=conf.get('MYSQL','host'),
        user=conf.get('MYSQL', 'user'),
        password=conf.get('MYSQL','password'),
        db=conf.get('MYSQL','db'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


    select_sql = "select * from `page` where 1=1 " 
    
    #select_sql += " where year = '2009' and season = '1'" 
    select_sql += " and  year in (2009) "

    select_sql += " and  season in (1)"


    cursor = connection.cursor()
    cursor.execute(select_sql)

    pages = cursor.fetchall()

    allowed_domains = ['hideystudio.com']
    
    localMode = conf.getboolean('SETTING', 'localmode')

    if localMode:
        allowed_domains = ['localhost']

        start_urls = []

        for page in pages:

            start_urls.append('http://localhost/python/drama_ratings/ys/rank/'+page['url'])

    else:
        allowed_domains = ['hideystudio.com']

        start_urls = []
        
        for page in pages:

            start_urls.append('http://www.hideystudio.com/rank/'+page['url'])


    def template_parse(self,response,page_id):

        list_all = []

        content = response.css('.content_bg_repeat')

        has_table = len(content.xpath('.//table[@id="table"]'))==1 if True else False 

        if has_table == False:

            #tr_all = response.css('.content_bg_repeat').xpath('tr')[1].xpath('.//table/tr')
            table_one = response.css('.content_bg_repeat').xpath('tr')[1].xpath('.//table')[0]
            
            tr_all = table_one.xpath('./tr')
            
            if len(tr_all) > 1:

                #column_map = []

                column_map = table_one.xpath(
                    './tr[@class="rank-top"]').xpath('.//div[@class="rank-top"]/strong/text()').extract()

                #print(column_map)
               
                tv_key = False
                time_key = False
                drama_key = False
                episode_keys = {}
                if len(column_map) > 0:
                    for ind, col_one in enumerate(column_map):
                        if col_one == '电视台':
                            tv_key = ind
                        elif col_one == '时段':
                            time_key = ind
                        elif col_one == '剧名':
                            drama_key = ind
                        elif col_one in ["1","2","3","4","5","6","7","8","9","10","11","12","13"]:
                            episode_keys[ind] = col_one
                        elif col_one == '平均':
                            rating_avg_key = ind
                        elif col_one == '走势':
                            trend_key = ind

                #return []


                for tr_one in tr_all:

                    tr_class = tr_one.xpath('@class').extract()

                    if ('rank-top' in tr_class) == True:
                        continue

                    #获取"电视台"字段
                    tv_name_temp = tr_one.xpath('./td')[tv_key].xpath('./div/text()').extract()#.extract_first()

                    if len(tv_name_temp) == 1:
                        tv_name = tv_name_temp[0]
                    else:
                        continue

                    tv_item = TvItem(name=tv_name)

                    #获取"时段"字段
                    time_name_temp = tr_one.xpath('./td')[time_key].xpath('./div/text()').extract()

                    if len(time_name_temp) == 1:
                        time_name = time_name_temp[0]
                    else:
                        continue

                    time_item = TimeItem(name=time_name)
                    
                    #获取"剧名"字段
                    drama_name_temp = tr_one.xpath('./td')[drama_key].xpath('./div/text()').extract()

                    drama_name = ''

                    if len(drama_name_temp) > 0:

                        for drama_one in drama_name_temp:
                            drama_name += re.sub('\s|\n','',drama_one)
                    else:
                        continue


                    #获取"集数"
                    epi_list = {}
                    #print(episode_keys)
                    for epi_key in episode_keys:
                        epi_rating_temp = tr_one.xpath('./td')[epi_key].xpath('./div/text()').extract()

                        if len(epi_rating_temp) == 1:
                            #epi_rating = 
                            epi_list[episode_keys[epi_key]] = epi_rating_temp[0]
                        
                        
                    #获取"平均收视率"
                    rating_avg = ''
                    rating_avg_temp = tr_one.xpath(
                        './td')[rating_avg_key].xpath('./div/text()').extract()

                    if len(rating_avg_temp) == 1:
                        rating_avg = rating_avg_temp[0]

                    #获取"走势"
                    trend = ''
                    trend_temp = tr_one.xpath(
                        './td')[trend_key].xpath('./div/text()').extract()

                    if len(trend_temp) == 1:
                        trend = trend_temp[0]

                    drama_item = DramaItem(
                        title=drama_name, page_id=page_id, epi_list=epi_list, rating_avg=rating_avg,trend=trend)
                    all_item = AllItem()
                    all_item['tv'] = tv_item
                    all_item['time'] = time_item
                    all_item['drama'] = drama_item
                    ''' print('222222222')
                    print(epi_list)

                    print('333333') '''
                    #all_item['epi_list'] = epi_list
                    list_all.append(all_item)

        return list_all

    def get_page_id(self, page_url):
        cursor = self.connection.cursor()

        sql = "select id from `page` where url = %s"

        cursor.execute(sql,(page_url))

        re_one = cursor.fetchone()

        if re_one:

            return re_one['id']

        return False            

    def parse(self, response):

        page_url = response.url.split("/")[-1]

        page_id = self.get_page_id(page_url)

        if page_id:
            print('page_id :',page_id)
            list_all = self.template_parse(response,page_id)

            if len(list_all) > 0:
                for one_item in list_all:
                    yield one_item

        else:
            print('not in page table')
        
        ''' print(11)
        yield all_item
        print(22) '''


            

