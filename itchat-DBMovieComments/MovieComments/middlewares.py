# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
import logging,requests
from random import sample,choice
import string
import faker
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

class ProxyMiddleware(object):

    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            self.logger.debug('使用代理:' + proxy)
            request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )

class CookiesMiddleware(object):
    def get_bids(self):
        bids="".join(sample(string.ascii_letters,11))
        return {"bid":bids}

    def process_request(self, request, spider):
        self.logger.debug("use cookies")
        request.cookies =self.get_bids()


