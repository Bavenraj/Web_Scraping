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
    start_urls = ["https://edition.cnn.com/2024/09/02/investing/volkswagen-factory-closure-germany/index.html"]

    # Corrected 'rules' attribute
    rules = [
        Rule(
            LinkExtractor(
                allow=r'\/2024\/[0-9]{2}\/[0-9]{2}\/[a-zA-Z\-]+\/[a-zA-Z\-]+\/index.html'
            ), 
            callback='parse_info', 
            follow=True
        )
    ]

    def parse_info(self, response):
        article = NewsArticle()
        article['url'] = response.url  # Removed the trailing comma
        article['source'] = 'CNN'  # Removed the trailing comma
        article['title'] = response.xpath('//h1[@data-editable="headlineText"]/text()').get().strip()  # Removed the trailing comma
        article['description'] = response.xpath('//meta[@name="description"]/@content').get()  # Removed the trailing comma
        article['date'] = response.xpath('//meta[@property="article:published_time"]/@content').get()  # Removed the trailing comma
        article['author'] = response.xpath('//meta[@name="author"]/@content').get()  # Removed the trailing comma

        raw_text = w3lib.html.remove_tags(response.xpath('//div[@class="article__content"]').get())
        cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
        article['text'] = cleaned_text
        return article
