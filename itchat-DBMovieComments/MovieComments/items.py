# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class MoviecommentsItem(scrapy.Item):

    collection=""

    name=scrapy.Field()
    href=scrapy.Field()
    favored_num=scrapy.Field()
    comment_time=scrapy.Field()
    comment_score=scrapy.Field()
    comment_content=scrapy.Field()
    imgurl=scrapy.Field()

    attention_num = scrapy.Field()
    install_time = scrapy.Field()
    city = scrapy.Field()
