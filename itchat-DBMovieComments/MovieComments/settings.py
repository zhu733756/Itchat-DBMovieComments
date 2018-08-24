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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'movie.douban.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

SPIDER_MIDDLEWARES = {
   'MovieComments.middlewares.CookiesMiddleware': 553,
   'MovieComments.middlewares.ProxyMiddleware': 554,
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

COOKIES_DEBUG=True

PROXY_POOL_URL="http://localhost:5555/random"
RETRY_HTTP_CODES = [401, 403, 408, 414, 500, 502, 503, 504]
cookie_str='bid=2Y0JTfLwAE8; ps=y; __guid=223695111.3617450202817394700.1535081223998.4727; __utmc=30149280; __utmc=223695111; push_noty_num=0; push_doumail_num=0; ll="118254"; __yadk_uid=u84YXRa4Quos6jSpv1ugAdmX3r598GAa; ct=y; _vwo_uuid_v2=D65567177BD83881FD786AFC69071D7F6|4544596066584f164efbd8799fc64c1d; __utmz=30149280.1535085837.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utmz=223695111.1535085837.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utmv=30149280.14809; dbcl2="148093400:qlrMmnwHSoU"; ck=I1hN; __utma=30149280.766659013.1535081224.1535095701.1535099912.5; __utmb=30149280.2.10.1535099912; monitor_count=30; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1535101479%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252Fsubject%252F26654269%252Fcomments%253Fstatus%253DP%22%5D; _pk_id.100001.4cf6=772f3f339728c624.1535081224.5.1535101479.1535096833.; _pk_ses.100001.4cf6=*; __utma=223695111.333086659.1535081224.1535095702.1535101479.5; __utmb=223695111.0.10.1535101479'
cookie_str2='bid=2Y0JTfLwAE8; __guid=236236167.4536013590969823000.1535081216832.8904; ps=y; __utmc=30149280; push_noty_num=0; push_doumail_num=0; ll="118254"; ct=y; _vwo_uuid_v2=D65567177BD83881FD786AFC69071D7F6|4544596066584f164efbd8799fc64c1d; dbcl2="148093400:5BI6mJMWbR0"; ck=Z6lp; as="https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26654269%2Fcomments%3Fstatus%3DP"; __utmz=30149280.1535085837.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; _pk_ses.100001.8cb4=*; __utma=30149280.766659013.1535081224.1535085837.1535090098.3; __utmv=30149280.14809; ap_v=1,6.0; monitor_count=11; _pk_id.100001.8cb4=9cbefaeb4631ae8e.1535090097.1.1535093565.1535090097.; __utmt=1; __utmb=30149280.16.10.1535090098'