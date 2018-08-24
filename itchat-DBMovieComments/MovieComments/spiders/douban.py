# -*- coding: utf-8 -*-
import scrapy
from MovieComments.items import MoviecommentsItem
import logging,time,random
from scrapy_redis.spiders import RedisCrawlSpider,RedisSpider
import re
from collections import deque
from run import itchat
from scrapy.utils.project import get_project_settings

class DoubanSpider(RedisSpider):

    name = 'douban'
    # allowed_domains = ['movie.douban.com','www.douban.com']
    redis_key = 'douban_spider:start_urls'

    def __init__(self, *args, **kwargs):
        self.former_tablename = ""
        super(DoubanSpider, self).__init__(*args, **kwargs)

    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True, meta={'dont_merge_cookies':'True'})

    def parse(self, response):
        new_tablename = "comments_{}". \
            format(re.findall(r".*?/(\d+)/com.*?", response.urljoin(""))[0])
        if new_tablename != self.former_tablename and self.former_tablename:
            itchat.auto_login(hotReload=True)
            itchat.send("Former desired request({}) has finished!"
                        .format(self.former_tablename), "filehelper!")
            self.former_tablename = new_tablename
        setattr(self, "collection", new_tablename)

        pageContent = response.xpath('//div[@class="comment-item"]')
        nextUrl = response.xpath('//a[@class="next"]/@href').extract_first()
        for comments in pageContent:
            item = MoviecommentsItem()
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
            self.logger.debug("Get nexturl:",nextUrl)
            time.sleep(random.choice([3, 4, 5]))
            cookie_str=get_project_settings().get("cookie_str2")
            cookie= \
                {key.strip().split("=", 1)[0]: key.strip().split("=", 1)[1]
                 for key in cookie_str2.strip().split(";")}
            self.logger.debug("change cookies")
            yield scrapy.Request(url=nextUrl,
                                 meta={"item": item, },
                                 cookies=cookie,
                                 callback=self.parse)

    # def loggin(self):
    #     login_url = "https://www.douban.com/accounts/login"
    #     return scrapy.FormRequest(url=login_url,
    #                              formdata={
    #                                  "form_email": "13627275733",
    #                                  "form_password": "zh1079333812",
    #                                  "source":"movie",
    #                                  "redir": "",
    #                                  "login": "登录"
    #                              },
    #                              meta={"cookiejar":0},
    #                              callback=self.get_cookie)
    #
    # def get_cookie(self, response):
    #     return response.meta["cookiejar"]

    def parse_info(self,response):
        item=response.meta["item"]
        item["city"]=response.css("div.basic-info div.user-info a::text").extract_first()
        install_time=response.css('div.basic-info div.pl::text').extract()
        if install_time:
            item["install_time"]=install_time[-1][:-2].strip()#profile > div > div.bd > div.basic-info > div > div
        else:
            item["install_time"]=""
        item["attention_num"]=response.css('#content div div.aside p.rev-link a::text').re_first(r"\d+")
        yield item


