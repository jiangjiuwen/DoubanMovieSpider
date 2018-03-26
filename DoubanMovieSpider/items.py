# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmoviespiderItem(scrapy.Item):
    # define the fields for your item here like:
    pass

class MovieItem(scrapy.Item):
    page_url = scrapy.Field()
    index = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    cover_url = scrapy.Field()
    cover_path = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    actors = scrapy.Field()
    type = scrapy.Field()
    region = scrapy.Field()
    release_date = scrapy.Field()
    runtime = scrapy.Field()
    alias = scrapy.Field()
    imdb_link = scrapy.Field()
    rating_num = scrapy.Field()
    rating_sum = scrapy.Field()
    quote = scrapy.Field()
    related_info = scrapy.Field()