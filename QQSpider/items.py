# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqspiderItem(scrapy.Item):
    # define the fields for your item here like:
    album_name = scrapy.Field()
    image_urls = scrapy.Field()
    image = scrapy.Field()
    account = scrapy.Field()
    # pass
