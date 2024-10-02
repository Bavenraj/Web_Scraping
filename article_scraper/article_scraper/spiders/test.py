import scrapy
import w3lib

class IetfSpider(scrapy.Spider):
    name = "ietf"
    allowed_domains = ["pythonscraping.com"]
    start_urls = ["https://pythonscraping.com/linkedin/ietf.html"]

    def parse(self, response):
        title1 = response.css('span.title::text').get()
        title2 = response.xpath('//span[@class="subheading"]/text()').get()
       

