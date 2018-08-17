# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from MovieComments.items import MoviecommentsItem

class MoviecommentsPipeline(object):

    def __init__(self,host,port,dbname,table):
        self.host = host
        self.port = port
        self.dbname=dbname
        self.table=table

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            host=settings.get("MONGODB_HOST"),
            port=settings.get("MONGODB_PORT"),
            dbname=settings.get("MONGODB_DBNAME"),
            table=settings.get("MONGODB_TABLENAME")
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db= self.client[self.dbname]

    def process_item(self, item, spider):
        if isinstance(item, MoviecommentsItem):
            try:
                info = dict(item)
                self.db[self.table].insert(info)
            except Exception as e:
                pass
        return item

    def close_spider(self,spider):
        self.client.close()
