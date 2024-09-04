# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsArticle(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    text = scrapy.Field()
    
class SitemapNewsArticle(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    text = scrapy.Field()
    
class NewsArticleCount(scrapy.Item):
    xml_url = scrapy.Field()
    article_count = scrapy.Field()
