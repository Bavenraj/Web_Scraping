import scrapy
from scrapy.spiders import CrawlSpider, Rule, SitemapSpider
from scrapy.linkextractors import LinkExtractor
from news_scraper.items import SitemapNewsArticle
import w3lib
from w3lib.html import remove_tags 
import re

class CnnsitemapSpider(SitemapSpider):
    name = "cnnSitemap"
    allowed_domains = ["edition.cnn.com"]
    sitemap_urls = ["https://edition.cnn.com/sitemaps/article-2024-02.xml"]
    
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT' : 20,
        'FEEDS' : {
            'news_article_Sitemap.csv': 
                {
                    'format': 'csv',
                    'encoding': 'utf-8',
                }
                }
    }
    
    def parse(self, response):
        article = SitemapNewsArticle()
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
