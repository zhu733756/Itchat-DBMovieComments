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

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
}

SPIDER_MIDDLEWARES = {
   'MovieComments.middlewares.CookiesMiddleware': 554,
}

ITEM_PIPELINES = {
   'MovieComments.pipelines.MoviecommentsPipeline': 300,
}

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

cookie_str='ll="118254"; bid=zeLloSw_6W0; ps=y; dbcl2="148093400:r9rDWAWnEf4"; ck=N7pn; __guid=223695111.630633805874402300.1534213202163.5835; __yadk_uid=PRAJivMtK9F5zKNvvWrUroGakz8mcywu; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1534303706%2C%22https%3A%2F%2Fm.douban.com%2Fsearch%2F%3Fquery%3D%25E5%2581%2587%25E9%259D%25A2%22%5D; _vwo_uuid_v2=D5E06D51A453672A3F5502017A0F3BC9A|3ae5f9ee4ab2fbe559a3ad9391459d6a; monitor_count=19; _pk_id.100001.4cf6=0eb62c833b7a7911.1534213204.5.1534303728.1534294996.; __utma=30149280.1328539538.1534213204.1534294958.1534303706.5; __utmc=30149280; __utmz=30149280.1534234898.3.2.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/1294438/comments; __utmv=30149280.14809; __utma=223695111.104934647.1534213204.1534294961.1534303706.5; __utmc=223695111; __utmz=223695111.1534213204.1.1.utmcsr=m.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search/; push_noty_num=0; push_doumail_num=0'
cookies = {key.strip().split("=",1)[0]: key.strip().split("=",1)[1] for key in cookie_str.strip().split(";")}