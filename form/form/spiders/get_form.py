import scrapy


class GetFormSpider(scrapy.Spider):
    name = "get_form"
    allowed_domains = ["pythonscraping.com"]
    start_urls = ["https://pythonscraping.com"]

    def parse(self, response):
        pass
