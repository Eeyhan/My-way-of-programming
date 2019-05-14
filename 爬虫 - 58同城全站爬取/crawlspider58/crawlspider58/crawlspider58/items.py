# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawlspider58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    img_url = scrapy.Field()
    url_detail = scrapy.Field()
    froms = scrapy.Field()
    price = scrapy.Field()
    payment = scrapy.Field()
    method = scrapy.Field()
    house_type = scrapy.Field()
    community = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    telphone = scrapy.Field()
    subway_distance = scrapy.Field()
    company = scrapy.Field()
    contact = scrapy.Field()
