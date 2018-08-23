# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
import logging,requests
from scrapy.spidermiddlewares.httperror import HttpError

class CookiesMiddleware(object):

    def __init__(self,cookie_dict):
        self.cookies=cookie_dict
        self.logger=logging.getLogger(__name__)


    def process_request(self,request,spider):
        self.logger.info("use cookies")
        request.cookies = getattr(spider,"get_cookie",self.cookies)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            cookie_dict = settings.get("cookies"),
        )

class ProxyMiddleware(object):

    def __init__(self,proxy_url):
        self.proxy_url=proxy_url
        self.logger=logging.getLogger(__name__)

    def get_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理 ' + proxy)
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get("PROXY_POOL_URL"),
        )

