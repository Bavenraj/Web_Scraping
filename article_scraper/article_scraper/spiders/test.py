import scrapy
import w3lib

class IetfSpider(scrapy.Spider):
    name = "ietf"
    allowed_domains = ["pythonscraping.com"]
    start_urls = ["https://pythonscraping.com/linkedin/ietf.html"]

    def parse(self, response):
        title1 = response.css('span.title::text').get()
        title2 = response.xpath('//span[@class="subheading"]/text()').get()
       
        return {"title1": response.css('span.title::text').get(),
                "number": response.xpath('//span[@class="rfc-no"]/text()').get(),
                "title2" : response.xpath('//span[@class="subheading"]/text()').get(),
                "date": response.xpath('//span[@class="date"]/text()').get(),
                "description": response.xpath('//meta[@name="DC.Description.Abstract"]/@content').get(),
                'author': response.xpath('//meta[@name="DC.Creator"]/@content').get(),
                'company': response.xpath('//span[@class="author-company"]/text()').get(),
                'address': response.xpath('//span[@class="address"]/text()').get(),
                'text':w3lib.html.remove_tags(response.xpath('//div[@class="text"]').get()),
                'headings': response.xpath('//span[@class="subheading"]/text()').getall()}
