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

    def __init__(self,host,port,dbname):
        self.host = host
        self.port = port
        self.dbname=dbname

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            host=settings.get("MONGODB_HOST"),
            port=settings.get("MONGODB_PORT"),
            dbname=settings.get("MONGODB_DBNAME"),
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db= self.client[self.dbname]

    def process_item(self, item, spider):
        collection=getattr(item,"collection","comments_")
        if isinstance(item, MoviecommentsItem):
            try:
                info = dict(item)
                self.db[collection].insert(info)
            except Exception as e:
                pass
        return item

    def close_spider(self,spider):
        self.client.close()

class ImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        url=request.url
        return url.split("/")[-1]

    def item_completed(self, results, item, info):
        image_paths=[x["path"] for ok,x in results if ok]
        if not image_paths:
            raise DropItem("Image downloaded failed!")

    def get_media_requests(self, item, info):
        yield scrapy.Request(item["imgurl"])