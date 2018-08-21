# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from MovieComments.items import MoviecommentsItem
from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import signals
from scrapy_redis.queue import SpiderQueue

class MoviecommentsPipeline(object):

    def __init__(self,host,port,db):
        self.host = host
        self.port = port
        self.db=db

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            host=settings.get("MONGODB_HOST"),
            port=settings.get("MONGODB_PORT"),
            db=settings.get("MONGODB_DBNAME"),
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.table= self.client[self.db]

    def process_item(self, item, spider):
        if isinstance(item, MoviecommentsItem):
            try:
                info = dict(item)
                self.table[item.collection].insert(info)
            except Exception as e:
                pass
        return item

    def close_spider(self,spider):
        self.client.close()
