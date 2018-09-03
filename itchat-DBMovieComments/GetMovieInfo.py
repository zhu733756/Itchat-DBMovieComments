# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""

import re,json,os
import requests
from requests import RequestException
from bs4 import BeautifulSoup
from urllib.parse import quote
from random import sample
import string

class GetMvInfo(object):

    def __init__(self):
        self.headers={
             "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
        with requests.session() as s:
            self.s=s

    def get_cookies(self):
        return {"bid":"".join(sample(string.ascii_letters+string.digits+"-_",11))}

    def html_response(self,url):
        try:
            page_content = requests.get(url).text
        except RequestException as e:
            print("Err:", e.args)
            return None
        else:
            regex=r"检测到有异常请求"
            cookies = self.get_cookies()
            if re.search(regex,page_content.strip()):
                print("use cookies:", cookies)
                page_content=self.s.get(url,headers=self.headers,cookies=cookies).text
            return BeautifulSoup(page_content, "html.parser")

    def getMovieTopic(self,SearchTopic):
        base_url = "https://m.douban.com/search/?query={}&type=movie".format(quote(SearchTopic))
        page_content=self.html_response(base_url)
        SearchIndex = []
        try:
            item=page_content.select("ul.search_results_subjects li")
            for no,li in enumerate(item):
                title=li.find("span",{"class":"subject-title"}).string
                score=li.find_all("span")[-1].string
                href="https://movie.douban.com/subject/"+li.find("a").get("href").split("/")[-2]+"/"
                SearchIndex.append({"No":str(no+1),"title":title,"score":score,"href":href})
            return json.dumps(SearchIndex,ensure_ascii=False)
        except Exception as e:
            return "Err:%s"%e.args

    def getMovieInfo(self,page_content):
        movie_info = []
        if page_content:
            try:
                item = page_content.find("div", {"id": "info"}).stripped_strings
                for string in item:
                    if string in ["编剧", "主演", "类型:", "制片国家/地区:", \
                                  "语言:", "上映日期:", "片长:", "又名:", "IMDb链接:"]:
                        string = "\n" + string
                    movie_info.append(string)
                return "".join(movie_info)
            except Exception  as e:
                print(e.args)
        return None

    def getShortSummary(self,page_content):
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

    def get_title(self,search_number):
        url="https://movie.douban.com/subject/{}/".format(search_number)
        page_content=self.html_response(url)
        try:
            text=page_content.find("span",{"property":"v:itemreviewed"}).string
            if text:
                return text.strip()
        except:
            return None

    def get_basic_info(self,url):
        page_content = self.html_response(url)
        info,summary=self.getMovieInfo(page_content),\
                           self.getShortSummary(page_content),
        return info,summary

    def close_session(self):
        self.s.close()

# t=GetMvInfo().get_basic_info("https://movie.douban.com/subject/25966209/")
# print(t)
