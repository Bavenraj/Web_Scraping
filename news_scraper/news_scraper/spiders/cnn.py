import scrapy


class CnnSpider(scrapy.Spider):
    name = "cnn"
    allowed_domains = ["edition.cnn.com"]
    start_urls = ["https://edition.cnn.com/world/asia"]

    def parse(self, response):
        pass
