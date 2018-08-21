# -*- coding: utf-8 -*-
import scrapy
from MovieComments.items import MoviecommentsItem
import logging,time,random
from scrapy_redis.spiders import RedisCrawlSpider,RedisSpider
import re
from collections import deque
from ItchatRoom import itchat

class DoubanSpider(RedisSpider):

    name = 'douban'
    # allowed_domains = ['movie.douban.com','www.douban.com']
    redis_key = 'douban_spider:start_urls'
    # logger = logging.getLogger(__name__)

    def __init__(self,former_deque="",tablename="", *args, **kwargs):

        self.former_deque = former_deque
        self.tablename= self.server.get(redis_key)
        super(DoubanSpider, self).__init__(*args, **kwargs)

    def get_tablename(self,response):
        tablename = "comments_" + re.findall(r".*?/(\d+)/comments.*?", response.urljoin(""))[0]
        if tablename:
            if len(self.former_deque):
                if self.former_deque != tablename:
                    itchat.send("Table(%s) is ok!"%self.former_deque,"filehelper")
                    self.former_deque=tablename
            else:
                self.former_deque=tablename
        print("========")
        print(tablename)
        print("========")
        print(self.former_deque)
        return tablename

    def parse(self, response):
        time.sleep(random.choice([3,4,5]))
        self.tablename=self.get_tablename(response)
        pageContent=response.xpath('//div[@class="comment-item"]')
        nextUrl = response.xpath('//a[@class="next"]/@href').extract_first()
        for comments in pageContent:
            item = MoviecommentsItem()
            item["name"] = comments.css("div.avatar a::attr(title)").extract_first()
            item["imgurl"]=comments.css("div.avatar img::attr(src)").extract_first()
            item["href"] = comments.css("div.avatar a::attr(href)").extract_first()
            item["comment_time"] = comments.css("span.comment-info span.comment-time::text").extract_first().strip()
            item["comment_content"] = comments.css("p span.short::text").extract_first().strip()
            item["comment_score"]=comments.css('span.comment-info span.rating::attr(class)').re_first(r"\d+")
            item["favored_num"]=comments.css('span.comment-vote span.votes::text').extract_first()
            yield scrapy.Request(url=item["href"],
                                 meta={"item":item},
                                 callback=self.parse_info)
        if nextUrl:
            nextUrl=response.urljoin(nextUrl)
            self.logger.info("Next page:",nextUrl)
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    def parse_info(self,response):

        item=response.meta["item"]
        item["city"]=response.css("div.bd div.basic-info div a::text").extract_first()
        install_time=response.css('div.bd div.basic-info div.pl::text').extract()
        if install_time:
            item["install_time"]=install_time[-1][:-2].strip()
        else:
            item["install_time"]=""
        item["attention_num"]=response.css('#content div div.aside p.rev-link a::text').re_first(r"\d+")
        yield item