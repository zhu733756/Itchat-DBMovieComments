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
DOWNLOAD_DELAY = 3
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

# COOKIES_DEBUG=True
REDIRECT_ENABLED=False#禁止重定向

PROXY_POOL_URL="http://localhost:5555/random"
RETRY_HTTP_CODES = [401, 403, 408, 414, 500, 502, 503, 504]

# cookie_str='bid=UoN1CxxSEjw; _ga=GA1.2.789031400.1535330723; _gid=GA1.2.1021477277.1535330723; push_noty_num=0; push_doumail_num=0; __utmc=30149280; ll="118254"; __guid=223695111.2708875744654674000.1535330746268.7314; __utmc=223695111; __yadk_uid=iS5WHaybkKGZXtf5zso9BjGaJoNfXtnX; _vwo_uuid_v2=D7B8175EA5E99DCE00CEB381B795E0A30|e5d5ae371636761bc0a52467905e365e; ap_v=1,6.0; _pk_ses.100001.4cf6=*; __utma=30149280.789031400.1535330723.1535341025.1535341025.1; __utmb=30149280.0.10.1535341025; __utmz=30149280.1535341025.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.789031400.1535330723.1535341025.1535341025.1; __utmb=223695111.0.10.1535341025; __utmz=223695111.1535341025.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); monitor_count=3; _pk_id.100001.4cf6=06cade9ebe4cf358.1535341025.1.1535341051.1535341025.'
# cookie_str_2='bid=UoN1CxxSEjw; _ga=GA1.2.789031400.1535330723; _gid=GA1.2.1021477277.1535330723; push_noty_num=0; push_doumail_num=0; __utmc=30149280; ll="118254"; __guid=223695111.2708875744654674000.1535330746268.7314; __utmc=223695111; __yadk_uid=iS5WHaybkKGZXtf5zso9BjGaJoNfXtnX; _vwo_uuid_v2=D7B8175EA5E99DCE00CEB381B795E0A30|e5d5ae371636761bc0a52467905e365e; ap_v=1,6.0; _pk_ses.100001.4cf6=*; __utma=30149280.789031400.1535330723.1535341025.1535341025.1; __utmb=30149280.0.10.1535341025; __utmz=30149280.1535341025.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.789031400.1535330723.1535341025.1535341025.1; __utmb=223695111.0.10.1535341025; __utmz=223695111.1535341025.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ps=y; dbcl2="148093400:iap0/5fdx/A"; ck=i6Mv; monitor_count=5; _pk_id.100001.4cf6=06cade9ebe4cf358.1535341025.1.1535341347.1535341025.'