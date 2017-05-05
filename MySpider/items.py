# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MySpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    url = Field()
    content = Field()


class NewsItem(Item):
    source = Field()
    title = Field()
    url = Field()
    content = Field()