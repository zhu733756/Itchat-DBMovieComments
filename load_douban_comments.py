# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""

import requests, re
from bs4 import BeautifulSoup
import logging, MainLoggerConfig
from pymongo import MongoClient
import time, random
import sys


loggerConfig.setup_logging(default_path="./log.yaml")

class get_douban_spider(object):

    logger = logging.getLogger()


    def __init__(self, url):

        self.url = url
        self.s = requests.session()
        self.headers = {
            "User-Agent": \
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }
        try:
            with open("./cookies.txt", "r") as f:
                self.cookies = {i.split("=")[0]: i.split("=")[1] for i in f.read().split(";")}
        except Exception as e:
            self.logger.error("invalid cookies!:%s" % e)
        try:
            self.client = MongoClient("localhost:27017", connect=True)["testdb"]["DouBandb"]
        except Exception as e:
            self.logger.error("Failed to connect Mongodb:%s" % e)

    def html_parse(self, base_url, params=None):

        content = self.s.get(base_url, headers=self.headers, params=params, cookies=self.cookies).text
        comment_html = BeautifulSoup(content, "html.parser")
        return comment_html

    def get_page_comment(self):

        commentList=self.get_page_comment().find_all("div", "comment-item")
        print(len(commentList))
        for commentInfo in commentList:
            try:
                votes = commentInfo.find("span", "comment-vote").find("span", "votes").string
                com_info = commentInfo.find("span", "comment-info")

                name = com_info.find("a").string
                if self.check_name(name=comments["name"]):
                    self.logger.info("current data has inserted!")
                    continue
                href = com_info.find("a").get("href")
                commentPeoInfo = self.html_parse(href)
                install_time = list(commentPeoInfo.find("div", "user-info").find("div", "pl").stripped_strings)[-1][:-2]
                attention = commentPeoInfo.find("p", "rev-link").find("a").string
                attention_num = re.findall("\d+", attention)[0]

                comment_time = com_info.find("span", "comment-time").string.strip()
                star = com_info.find("span", title=True).get("title").strip()
                comment_content = commentInfo.find("p").string.strip()
                self.logger.info(
                    "Get data:{},{},{},{},{},{},{}".format(name, install_time, attention_num, votes, comment_time, star,
                                                           comment_content))
                comments = {"name": name,
                            "install_time": install_time,
                            "attention_num": attention_num,
                            "votes": votes,
                            "comment_time": comment_time,
                            "star": star,
                            "comment_content": comment_content
                            }
                print(comments)
            except:
                pass
            else:
                try:
                    self.client.insert_one(comments, bypass_document_validation=True)
                    self.logger.info("Successfully insert current downloaded data!")
                except Exception as e:
                    self.logger.error("Failed to insert current data to Mongodb:{}".format(e))
                    continue

    def check_name(self, name):

        return True if self.client.find_one({"name": name}) else False

    def get_pages(self):

        try:
            content = self.html_parse(self.url)
        except Exception as e:
            self.logger.error("Valid connection:%s" % e)
            self.logger.info("Click here(%s) to try in webdriver!" % self.url)
        else:
            # watchNum = re.findall(r"\d+", content.find("li", "is-active").get_text())[0]
            watchNum=20
            self.logger.info("Get max watchNum:%s" % watchNum)
            for i in range(int(int(watchNum) / 20)+1):
                time.sleep(random.choice([5, 6, 7, 8, 9]))
                params = dict(start=str(i), limit="20", sort="new_score", status="P")
                yield self.html_parse(base_url=self.url, params=params)
        finally:
            self.s.close()


if "__main__" == __name__:
    m = get_douban_spider("https://movie.douban.com/subject/6874741/comments")
    m.get_page_comment()
