# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
import logging

class CookiesMiddleware(object):

    def __init__(self,cookies_dict):
        self.cookies=cookies_dict
        self.logger=logging.getLogger(__name__)

    def process_request(self,request,spider):
        self.logger.info("use cookies")
        request.cookies = self.cookies

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            cookies_dict=settings.get("cookies")
        )
