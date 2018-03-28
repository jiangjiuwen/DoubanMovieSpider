# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader


def format_str(value):
    if (value):
        value = value.replace('\n', '') .strip()
    return value


def return_val(value):
    return value


class MovieItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class MovieItem(scrapy.Item):
    page_url = scrapy.Field()
    index = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field(
        input_processor=MapCompose(lambda x:x.lstrip('(').rstrip(')'))
    )
    cover_url = scrapy.Field(
        output_processor=MapCompose(return_val)
    )
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
    related_info = scrapy.Field(
        input_processor=MapCompose(format_str),
        output_processor=Join('\n')
    )