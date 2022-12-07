# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class SpiderSteamPipeline:

    def open_spider(self, spider):
        self.file = open('items.json', 'w')
        self.data = []

    def close_spider(self, spider):
        # json.dumps(self.data, self.file) - этот вариант работал. Как он понимал в какой файл писать - я без понятия
        # тут надо сказать, что он не принимает параметр file
        self.file.write(json.dumps(self.data))
        self.file.close()

    def process_item(self, item, spider):
        self.data.append(item)
        return item