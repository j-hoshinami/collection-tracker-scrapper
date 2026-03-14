# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyAnimeListItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    episode_quant = scrapy.Field()
    initial_date = scrapy.Field()
    end_date = scrapy.Field()
    available_on = scrapy.Field()
    genres = scrapy.Field()
    studio = scrapy.Field()
    premiered = scrapy.Field()
