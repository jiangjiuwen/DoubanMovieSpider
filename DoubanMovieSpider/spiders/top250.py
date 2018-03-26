# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from urllib import parse

from DoubanMovieSpider.items import MovieItem

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
        index = response.css('.top250-no::text').extract_first('')
        title = response.css('div#content h1')
        name = title.css('span::text').extract_first('')
        year = title.css('span.year::text').extract_first('').lstrip('(').rstrip(')')
        cover_url = response.css('#mainpic a img::attr(src)').extract_first('')
        rating_num = response.css('.rating_num::text').extract_first('')
        rating_sum = response.css('.rating_people span::text').extract_first('')
        related_info = response.css('#link-report span::text').extract_first('').strip()

        movie_item = MovieItem()
        movie_item['page_url'] = response.url
        movie_item['index'] = index
        movie_item['name'] = name
        movie_item['year'] = year
        movie_item['cover_url'] = [cover_url]
        # movie_item['director'] = director
        # movie_item['writer'] = writer
        # movie_item['actors'] = actors
        # movie_item['type'] = type
        # movie_item['region'] = region
        # movie_item['release_date'] = release_date
        # movie_item['alias'] = alias
        # movie_item['imdb_link'] = imdb_link
        movie_item['rating_num'] = rating_num
        movie_item['rating_sum'] = rating_sum
        movie_item['quote'] = response.meta.get('quote', '')
        movie_item['related_info'] = related_info
        yield movie_item
