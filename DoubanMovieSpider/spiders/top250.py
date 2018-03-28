# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from urllib import parse

from DoubanMovieSpider.items import MovieItem, MovieItemLoader

class Top250Spider(scrapy.Spider):
    name = 'top250'
    # Douban has spaned the default header of scrapy
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.header)

    def parse(self, response):
        # parse current page's movie urls
        movie_items = response.css('div.item .info')
        for movie_item in movie_items:
            movie_url = movie_item.css('div.hd a::attr(href)').extract_first('')
            movie_quote = movie_item.css('div.bd .quote span::text').extract_first('')
            yield Request(url=movie_url, headers=self.header, meta={'quote':movie_quote}, callback=self.parse_movie_item)

        # parse next page, then parse movie urls
        next_page_url = response.css('span.next a::attr(href)').extract_first('')
        next_page_url = parse.urljoin(response.url, next_page_url)
        if next_page_url:
            yield Request(url=next_page_url, headers=self.header, callback=self.parse)
        pass

    def parse_movie_item(self, response):
        il = MovieItemLoader(item=MovieItem(), response=response)
        il.add_value('page_url', response.url)
        il.add_css('index', '.top250-no::text')
        il.add_css('name', 'div#content h1 span::text')
        il.add_css('year', 'div#content h1 span.year::text')
        il.add_css('cover_url', '#mainpic a img::attr(src)')
        # movie_item['writer'] = writer
        # il.add_css('writer', '.writer')
        # il.add_css('actors', '.actors')
        # il.add_css('type', '.type')
        # il.add_css('region', '.region')
        # il.add_css('release_date', '.release_date')
        # il.add_css('alias', '.alias')
        # il.add_css('imdb_link', '.imdb_link')
        il.add_css('rating_num', '.rating_num::text')
        il.add_css('rating_sum', '.rating_sum .rating_people span::text')
        il.add_value('quote', response.meta.get('quote', ''))
        il.add_css('related_info', '#link-report span::text')
        movie_item = il.load_item()
        yield movie_item
