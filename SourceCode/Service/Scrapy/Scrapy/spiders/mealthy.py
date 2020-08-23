# -*- coding: utf-8 -*-
import scrapy


class MealthySpider(scrapy.Spider):
    name = 'mealthy'
    allowed_domains = ['']
    start_urls = ['http:///']

    def parse(self, response):
        pass
