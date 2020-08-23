# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipeItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    ingredients = scrapy.Field()
    time = scrapy.Field()
    steps = scrapy.Field()
    img_link = scrapy.Field()
    source = scrapy.Field()
    link = scrapy.Field()
