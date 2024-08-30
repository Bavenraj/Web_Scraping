import scrapy


class InstaSpider(scrapy.Spider):
    name = "insta"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://instagram.com/bavenraj08"]

    def parse(self, response):
        return { "Followers": response.xpath('//*[@id="mount_0_0_ZQ"]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]/div/a/span/span').get()}
