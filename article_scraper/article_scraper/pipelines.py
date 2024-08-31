# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from datetime import datetime

class CheckItem:
    def process_item(self, article, spider):
        if not article['lastUpdate'] or not article['url'] or not article['title']:
            raise DropItem("Missing Something!")
        return article
    
class CheckDate:
    def process_item(self,article, spider):
        article['lastUpdate'] = article['lastUpdate'].replace("This page was last edited on ", "").strip()
        article['lastUpdate'] = datetime.strptime(article['lastUpdate'], '%d %B %Y, at %H:%M')
        return article