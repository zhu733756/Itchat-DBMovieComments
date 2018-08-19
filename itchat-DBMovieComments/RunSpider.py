# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
from scrapy import cmdline

cmdline.execute("lpush douban_spider:start_urls %s"%CrawlUrl)
