import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_scraper.items import NewsArticle
import w3lib
from w3lib.html import remove_tags 
import re

class CnnSpider(CrawlSpider):
    name = "cnn"
    allowed_domains = ["edition.cnn.com"]
    start_urls = ["https://edition.cnn.com/world/africa/index.html"]
    rules = [
        Rule(
            LinkExtractor( #2024/09/03/first-article/first-title/index.html
                allow=r'\/2024\/[0-9]{2}\/[0-9]{2}\/[a-zA-Z\-]+\/[a-zA-Z\-]+\/index.html'
            ), 
            callback='parse_info', 
            follow=True
        )
    ]

    def parse_info(self, response):
        article = NewsArticle()
        article['url'] = response.url 
        article['source'] = 'CNN'  
        article['title'] = response.xpath('//h1[@data-editable="headlineText"]/text()').get().strip()  
        article['description'] = response.xpath('//meta[@name="description"]/@content').get()  
        article['date'] = response.xpath('//meta[@property="article:published_time"]/@content').get() 
        article['author'] = response.xpath('//meta[@name="author"]/@content').get()  
        responses = response.xpath('//div/p[@class="paragraph inline-placeholder vossi-paragraph-primary-core-light"]/text()').getall()
        for respond in responses:
            article['text']  = respond.replace('\n', ' ').strip()
        return article
