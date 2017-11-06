# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TvItem(scrapy.Item):
    name = scrapy.Field()


class TimeItem(scrapy.Item):
    name = scrapy.Field()


class DramaItem(scrapy.Item):
    #id = scrapy.Field()
    title = scrapy.Field()
    tv_id = scrapy.Field()
    time_id = scrapy.Field()
    page_id = scrapy.Field()
    epi_list = scrapy.Field()
    rating_avg = scrapy.Field()
    trend = scrapy.Field()


class AllItem(scrapy.Item):
    tv = scrapy.Field()#TvItem()
    time = scrapy.Field()#TimeItem()
    drama = scrapy.Field()#DramaItem()
    


class PageItem(scrapy.Item):
    #id = scrapy.Field()
    url = scrapy.Field()
    year = scrapy.Field()
    season = scrapy.Field()
