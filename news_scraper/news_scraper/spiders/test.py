import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["tesla.com"]
    start_urls = ["https://tesla.com"]

    def parse(self, response):
        pass
