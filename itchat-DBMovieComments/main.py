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
from ItchatReply import start
import logging

def start_spider(name="douban"):
    cmdline.execute("scrapy crawl {}".format(name).split())

def itchat_run():
    start()

if __name__ == "__main__":

    logging.getLogger("requests").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)
    p1=Process(target=start_spider,args=())
    p2=Process(target=itchat_run,args=())
    for p in (p1,p2):
        p.start()
    for p in (p1, p2):
        p.join()
