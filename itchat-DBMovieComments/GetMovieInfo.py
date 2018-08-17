# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""

import re
import requests
from requests import RequestException
from bs4 import BeautifulSoup

def html_response(url):
    try:
        page_content = requests.get(url).text
    except RequestException as e:
        print("Err:", e.args)
        return None
    return BeautifulSoup(page_content, "html.parser")

def getMovieInfo(page_content):
    movie_info = []
    if page_content:
        item = page_content.find("div", {"id": "info"}).stripped_strings
        for string in item:
            if string in ["编剧", "主演", "类型:", "制片国家/地区:", \
                          "语言:", "上映日期:", "片长:", "又名:", "IMDb链接:"]:
                string = "\n" + string
            movie_info.append(string)
        return "".join(movie_info)
    return None

def getShortSummary(page_content):
    if page_content:
        try:
            text=page_content.find("span",{"property":"v:summary"}).string
        except AttributeError as e:
            return "没有内容简介"
        else:
            if text:
                return text.strip()
            return "没有内容简介"
    return None
