import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_scraper.items import NewsArticle
import w3lib

class CnnSpider(CrawlSpider):
    name = "cnn"
    allowed_domains = ["edition.cnn.com"]
    start_urls = ["https://edition.cnn.com/world/asia"]
    rule = [Rule(LinkExtractor(allow=r'\/2020\/[0-9][0-9]\/[0-9][0-9]\/[a-zA-Z\-]+\/[a-zA-Z\-]+\/index.html'), callback='parse', follow=True)]

    def parse(self, response):
        article = NewsArticle()
        article['url'] = response.url,
        article['source'] = 'CNN',
        article['title'] = response.xpath('//h1[@data-editable="headlineText"]/text()').get(),
        article['description'] = response.xpath('//meta[@name="description"]/@content').get(),
        article['date'] = response.xpath('//meta[@property="article:published_time"]/@content').get(),
        article['author'] = response.xpath('//meta[@name="author"]/@content').get(),
        article['text'] = w3lib.html.remove_tags(response.xpath('//div[@class="article__content"]').get())
        return article
