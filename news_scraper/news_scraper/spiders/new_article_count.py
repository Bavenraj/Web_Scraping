import scrapy
from scrapy.spiders import CrawlSpider
from news_scraper.items import NewsArticleCount

def auto_start_urls():
    url = []
    years = ['2020', '2021', '2022', '2023']
    months = ['01','02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]
    for year in years:
        for month in months:
            url.append(f'https://edition.cnn.com/sitemaps/article-{year}-{month}.xml')
    return url
    #return ['https://edition.cnn.com/sitemaps/article-{}-{}.xml'.format(year, month) for year in years for month in months]
        
class NewArticleCountSpider(scrapy.Spider):
    name = "new_article_count"
    allowed_domains = ["edition.cnn.com"]
    start_urls = auto_start_urls()

    custom_settings = {
        'FEEDS' : {
            'news_article_count.csv': 
                {
                    'format': 'csv',
                    'encoding': 'utf-8',
                }
        }
    }
    
    def parse(self, response):
        article = NewsArticleCount()
        article['xml_url'] = response.url
        article['article_count'] = response.text.count('<url>')
        return article

# class NewArticleCountSpider(CrawlSpider):
#     name = "new_article_count"
#     allowed_domains = ["edition.cnn.com"]
#     start_urls = auto_start_urls()

#     custom_settings = {
#         'CLOSESPIDER_PAGECOUNT' : None,
#         'FEEDS' : {
#             'news_article_count.csv': 
#                 {
#                     'format': 'csv',
#                     'encoding': 'utf-8',
#                 }
#                 }
#     }
    
#     def parse(self, response):
#         article = NewsArticleCount()
#         article['url'] = response.url
#         article['count'] = response.text.count('<url>')
#         return article