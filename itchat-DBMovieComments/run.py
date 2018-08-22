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
from multiprocessing import Process

cmdline.execute("scrapy crawl douban".split())
Process()
