import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from article_scraper.items import ArticleScraperItem

class WikipediaSpider(CrawlSpider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Kevin_Bacon"]

    rules = [Rule(LinkExtractor(allow=r'wiki/((?!:).)*$'), callback='parse_info', follow=True)]
    
    custom_settings = {
        "FEED_URI" : "article.xml",
        "FEED_FORMAT" :  "xml"
    }
    
    def parse_info(self, response):
        article = ArticleScraperItem()
        article['title'] = response.xpath('//span[@class="mw-page-title-main"]/text()').get() or response.xpath('//h1/i/text()').get()
        article['url'] = response.url
        article['lastUpdate'] = response.xpath('//li[@id="footer-info-lastmod"]/text()').get()
        return article


