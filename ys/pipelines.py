# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors



class DramaPipeline(object):

    connection = pymysql.connect(
            host='localhost',
            user='gljgljglj',
            password='gljgogo',
            db='ys',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    cursor = connection.cursor()

    def process_item(self, item, spider):
        
        if spider.name != 'ys':
            pass
        
        tv_item = item['tv']
        time_item = item['time']
        drama_item = item['drama']

        tv_id = self.get_tv_id(tv_item['name'])
        
        print('tv_name :',tv_item['name'])
        if tv_id:
            print('tv_id :',tv_id)
            time_id = self.get_time_id(time_item['name'])
            print('time_name :',time_item['name'])
            if time_id:
                print('time_id :',time_id)
                drama_id = self.get_drama_id(drama_item['title'],drama_item['page_id'],{'tv_id':tv_id,'time_id':time_id})
                print('drama_name :',drama_item['title'])
                if drama_id:
                    print('drama_id :',drama_id)
                    return drama_id
        return None

    def get_tv_id(self, tv_name):
        '''
        #get_tv_id:根据剧名获取ID，没有则新建
        '''

        sql = "select id from `tv_station` where `name` = %s "

        re_count = self.cursor.execute(sql, (tv_name))

        tv_exist = True  if re_count else False

        #print('tv exsit:', tv_exist)

        if tv_exist:

            re_one = self.cursor.fetchone()

            return re_one['id']
        else:
            insert_sql = "insert into `tv_station` (`name`) values (%s)"

            self.cursor.execute(insert_sql, (tv_name))

            insert_id = self.cursor.lastrowid

            self.connection.commit()

            return insert_id

    def get_time_id(self, time_name):
        '''
        #get_time_id:根据时间段获取ID，没有则新建
        '''
       
        sql = "select id from `play_time` where `name` = %s "

        re_count = self.cursor.execute(sql, (time_name))

        time_exist = True  if re_count else False

        #print('tv exsit:', tv_exist)

        if time_exist:

            re_one = self.cursor.fetchone()

            return re_one['id']
        else:
            insert_sql = "insert into `play_time` (`name`) values (%s)"

            self.cursor.execute(insert_sql, (time_name))

            insert_id = self.cursor.lastrowid

            self.connection.commit()

            return insert_id

    def get_drama_id(self, drama_title, page_id, info):
        '''
        #get_drama_id:根据剧名获取ID，没有则新建
        '''
        

        sql = "select id from `drama` where `title` = %s "

        re_count = self.cursor.execute(sql, (drama_title))

        time_exist = True  if re_count else False

        #print('tv exsit:', tv_exist)

        if time_exist:

            re_one = self.cursor.fetchone()

            return re_one['id']
        else:
            insert_sql = "insert into `drama` (`title`,`tv_id`,`time_id`,`page_id`) values (%s,%s,%s,%s)"

            self.cursor.execute(insert_sql, (drama_title, info['tv_id'], info['time_id'], page_id))

            insert_id = self.cursor.lastrowid

            self.connection.commit()

            return insert_id