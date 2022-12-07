# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SpiderSteamItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    all_reviews_count = scrapy.Field()
    grade = scrapy.Field()
    release_date = scrapy.Field()
    developers = scrapy.Field()
    tags = scrapy.Field()
    platforms = scrapy.Field()
    recommendations = scrapy.Field()
    details = scrapy.Field()
    languages = scrapy.Field()
