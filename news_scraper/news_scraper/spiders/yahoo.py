import scrapy


class YahooSpider(scrapy.Spider):
    name = "yahoo"
    allowed_domains = ["malaysia.news.yahoo.com"]
    start_urls = ["https://malaysia.news.yahoo.com"]

    def parse(self, response):
        pass
