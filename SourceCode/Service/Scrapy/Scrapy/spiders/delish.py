# -*- coding: utf-8 -*-
import scrapy
from Scrapy.items import RecipeItem


class DelishSpider(scrapy.Spider):
    name = 'delish'
    allowed_domains = ['www.delish.com']
    start_urls = ['https://www.delish.com/cooking/recipe-ideas/']

    def parse(self, response):
        nodes = response.xpath("/html/body/main/div[4]/div/a")
        print(len(nodes))
        for node in nodes:
            recipe = node.xpath('./@href')
            img_link = node.xpath('./div[1]/img/@data-src').extract_first().strip()
            link = 'http://' + self.allowed_domains[0] + recipe.extract_first().strip()
            yield scrapy.Request(link, self.parse_recipe, meta={'img_link': img_link})

    def parse_recipe(self, response):
        try:
            recipe = RecipeItem()
            recipe['title'] = response.xpath("//div[@class='content-header-inner']/h1/text()").extract_first().strip()
            ingredients = response.xpath("//div[@class='ingredient-item']/span/p/text()")
            recipe['ingredients'] = ', '.join(i.extract().strip() for i in ingredients)
            time = response.xpath("//div[@class='recipe-details-item total-time']/span/text()").extract()
            recipe['time'] = f'{60*int(time[0].strip()) + int(time[1].strip())}'
            steps = response.xpath("//div[@class='direction-lists']/ol/li/text()")
            recipe['steps'] = '\n'.join([f'{i+1}: {s.extract().strip()}' for i, s in enumerate(steps)])
            recipe['source'] = 'delish'
            recipe['link'] = response.url
            recipe['img_link'] = response.meta['img_link']
            text_len = len(response.xpath("/html/body/main/div[5]/div[1]/div[2]/p"))
            text = ''
            for i in range(1, text_len+1):
                t = response.xpath(f"string(/html/body/main/div[5]/div[1]/div[2]/p[{i}])").extract_first()
                text += t if t else ''
            recipe['text'] = text.replace('"', '')
            if text:
                return recipe
            else:
                print(response.url)
        except:
            print(response.url)
