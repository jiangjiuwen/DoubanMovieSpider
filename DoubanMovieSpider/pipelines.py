# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

from scrapy.pipelines.images import ImagesPipeline

class DoubanmoviespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('movie.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        movie = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(movie)

    def spider_closed(self, spider):
        self.file.close()


class CoverImagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            cover_path = value['path']
        item['cover_path'] = cover_path
        return item