# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors

import configparser

class ListPipeline(object):

    conf = configparser.ConfigParser()
    conf.read('ys/conf.ini')

    connection = pymysql.connect(
        host=conf.get('MYSQL', 'host'),
        user=conf.get('MYSQL', 'user'),
        password=conf.get('MYSQL', 'password'),
        db=conf.get('MYSQL', 'db'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = connection.cursor()

    def process_item(self, item, spider):
        url = item['url']
        year = item['year']
        season = item['season']


        sql = "select id,url from `page` where `year` = %s and `season` = %s "

        re_count = self.cursor.execute(sql, (year,season))

        page_exist = True  if re_count else False

        #print('tv exsit:', tv_exist)

        if page_exist:

            re_one = self.cursor.fetchone()

            if url != re_one['url']:

                update_sql = "update `page` set `url` = %s where `id` = %s "

                self.cursor.execute(update_sql, (url, re_one['id']))

                self.connection.commit()

            #status置为1
            update_sql = "update `page` set `status` = 1 where `id` = %s "

            self.cursor.execute(update_sql, (re_one['id']))

            self.connection.commit()

            return re_one['id']

        else:

            insert_sql = "insert into `page` (`url`,`year`,`season`,`status`)" \
            " values (%s, %s, %s, 1)"

            self.cursor.execute(insert_sql, (url, year, season))

            insert_id = self.cursor.lastrowid

            self.connection.commit()

            return insert_id

