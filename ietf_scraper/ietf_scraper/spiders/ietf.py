import scrapy


class IetfSpider(scrapy.Spider):
    name = "ietf"
    allowed_domains = ["pythonscraping.com"]
    start_urls = ["https://pythonscraping.com/linkedin/ietf.html"]

    def parse(self, response):
        title1 = response.css('span.title::text').get()
        title2 = response.xpath('//span[@class="title"]/text()').get()
       
        return {"title1": title1,
                "title2": title2}
