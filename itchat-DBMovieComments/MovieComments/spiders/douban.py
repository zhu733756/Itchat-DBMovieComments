# -*- coding: utf-8 -*-
import scrapy
from MovieComments.items import MoviecommentsItem
import logging,time,random
from scrapy_redis.spiders import RedisCrawlSpider
import re

class DoubanSpider(RedisCrawlSpider):

    name = 'douban'
    # allowed_domains = ['movie.douban.com','www.douban.com']
    redis_key = 'douban_spider:start_urls'
    logger = logging.getLogger(__name__)
    table = ""

    def parse(self, response):
        self.table="Comments_"+re.search(r"\d+",response.url).group(0)
        time.sleep(random.choice([3,4,5]))
        pageContent=response.xpath('//div[@class="comment-item"]')
        nextUrl = response.xpath('//a[@class="next"]/@href').extract_first()
        self.logger.info("Total comments under current url:", len(list(pageContent)))
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
            nextUrl=response.url+nextUrl
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