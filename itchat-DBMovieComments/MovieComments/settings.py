# -*- coding: utf-8 -*-

# Scrapy settings for MovieComments project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'MovieComments'

SPIDER_MODULES = ['MovieComments.spiders']
NEWSPIDER_MODULE = 'MovieComments.spiders'

ROBOTSTXT_OBEY = False

USER_AGENT="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 5.2; Trident/4.0) AppleWebKit/534.36.5 (KHTML, like Gecko) Opera/8.80.(X11; Linux i686; os-RU) Presto/2.9.171 Version/12.00"

SPIDER_MIDDLEWARES = {
    'MovieComments.middlewares.ProxyMiddleware': 133,
    "MovieComments.middlewares.CookiesMiddleware": 135,
}

DOWNLOAD_TIMEOUT = 15
DOWNLOAD_DELAY = 1
# IMAGES_STORE="./images"

ITEM_PIPELINES = {
   'MovieComments.pipelines.MoviecommentsPipeline': 300,
   # 'MovieComments.pipelines.ImgPipeline': 303,
}

LOG_LEVEL="INFO"

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = "DBMovie"

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER= "scrapy_redis.scheduler.Scheduler"
#不清理redisqueues, 允许暂停或重启crawls
SCHEDULER_PERSIST= True
SCHEDULER_QUEUE_CLASS= 'scrapy_redis.queue.SpiderPriorityQueue'
#该项仅对queueclass is SpiderQueue or SpiderStack生效，阻止spider被关闭的最大空闲时间
SCHEDULER_IDLE_BEFORE_CLOSE= 10
#连接redis使用
REDIS_HOST = '127.0.0.1'
REDIS_PORT= 6379

REDIRECT_ENABLED=False#禁止重定向

PROXY_URL="http://localhost:5555/random"
RETRY_HTTP_CODES = [401, 403, 408, 414, 500, 502, 503, 504]

