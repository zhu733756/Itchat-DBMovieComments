# -*- coding: utf-8 -*-
import scrapy
from MovieComments.items import MoviecommentsItem
import logging,time,random
from scrapy_redis.spiders import RedisCrawlSpider,RedisSpider
import re
from ItchatReply import schedule
from scrapy.exceptions import DontCloseSpider

class DoubanSpider(RedisSpider):

    name = 'douban'
    # allowed_domains = ['movie.douban.com','www.douban.com']
    redis_key = 'douban_spider:start_urls'

    def __init__(self, *args, **kwargs):
        self.former_tbname=""
        super(DoubanSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        new_tablename = "comments_{}". \
            format(re.findall(r".*?/(\d+)/com.*?", response.urljoin(""))[0])
        if self.former_tbname != new_tablename:
            if self.former_tbname:
                schedule(self.former_tbname)
            self.former_tbname=new_tablename
        setattr(self, "collection", new_tablename)
        pageContent = response.xpath('//div[@class="comment-item"]')
        nextUrl = response.xpath('//a[@class="next"]/@href').extract_first()
        for comments in pageContent:
            item = MoviecommentsItem()
            # item["tbname"]=new_tablename
            item["name"] = comments.css("div.avatar a::attr(title)").extract_first()
            item["imgurl"] = comments.css("div.avatar img::attr(src)").extract_first()
            item["href"] = comments.css("div.avatar a::attr(href)").extract_first()
            item["comment_time"] = comments.css("span.comment-info span.comment-time::text").extract_first().strip()
            item["comment_content"] = comments.css("p span.short::text").extract_first().strip()
            item["comment_score"] = comments.css('span.comment-info span.rating::attr(class)').re_first(r"\d+")
            item["favored_num"] = comments.css('span.comment-vote span.votes::text').extract_first()
            yield scrapy.Request(url=item["href"],
                                 meta={"item": item,},
                                 callback=self.parse_info)
        if nextUrl:
            nextUrl = response.urljoin(nextUrl)
            yield scrapy.Request(url=nextUrl,
                                 callback=self.parse)

    def parse_info(self,response):
        item=response.meta["item"]
        item["city"]=response.css("div.basic-info div.user-info a::text").extract_first()
        install_time=response.css('div.basic-info div.pl::text').extract()
        if install_time:
            item["install_time"]=install_time[-1][:-2].strip()
        else:
            item["install_time"]=""
        item["attention_num"]=response.css('#content div div.aside p.rev-link a::text').re_first(r"\d+")
        yield item

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        # XXX: Handle a sentinel to close the spider.
        self.schedule_next_requests()
        len_urls = self.server.llen(self.redis_key)
        if len_urls == 0 and self.former_tbname:
            schedule(self.former_tbname)
            self.former_tbname=""
        raise DontCloseSpider
