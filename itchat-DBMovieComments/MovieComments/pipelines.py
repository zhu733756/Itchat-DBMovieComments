# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from MovieComments.items import MoviecommentsItem
from scrapy_redis.spiders import signals
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import  ImagesPipeline
import os,scrapy

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
        collection=getattr(spider,"collection","comments_id_lost")
        if isinstance(item, MoviecommentsItem):
            try:
                info = dict(item)
                self.db[collection].insert(info)
            except Exception as e:
                print(e.args)
        return item

    def close_spider(self,spider):
        self.client.close()

# class ImgPipeline(ImagesPipeline):
#
#     def file_path(self, request, response=None, info=None):
#         filename=request.url.split("/")[-1]
#         if response:
#             path="{}/{}".format(response.meta["tbname"],filename)
#             if not os.path.exists(path):
#                 os.makedirs(path)
#         return path
#
#     def item_completed(self, results, item, info):
#         image_paths=[x["path"] for ok,x in results if ok]
#         if not image_paths:
#             raise DropItem("Image downloaded failed!")
#
#     def get_media_requests(self, item, info):
#         yield scrapy.Request(item["imgurl"],meta={"tbname": item["tbname"],})

