# -*- coding: utf-8 -*-
import scrapy


class SeriouseatsSpider(scrapy.Spider):
    name = 'seriouseats'
    allowed_domains = ['']
    start_urls = ['http:///']

    def parse(self, response):
        pass
