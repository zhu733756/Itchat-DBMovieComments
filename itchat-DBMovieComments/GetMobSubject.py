# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""


import json
from urllib.parse import quote
from pyquery import PyQuery as pq

def getMovieTopic(SearchTopic):
    base_url = "https://m.douban.com/search/?query={}&type=movie".format(quote(SearchTopic))
    doc=pq(base_url)
    SearchIndex = []
    try:
        item=doc("ul.search_results_subjects li").items()
        if item:
            for no,li in enumerate(item):
                title=li.find(".subject-title").text()
                score=li.find("p span.rating-stars").siblings("span").text()
                href="https://movie.douban.com/subject/"+li.find("a").attr("href").split("/")[-2]+"/"
                SearchIndex.append({"No":str(no+1),"title":title,"score":score,"href":href})
            return json.dumps(SearchIndex,ensure_ascii=False)
    except Exception as e:
        return "Err:%s"%e.args


