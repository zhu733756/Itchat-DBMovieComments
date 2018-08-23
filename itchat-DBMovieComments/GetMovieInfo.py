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

cookie_str_former='talionnav_show_app="0"; ll="118254"; bid=MKV-C3S5_Dk; __utma=30149280.106230672.1534912220.1534912220.1534912220.1; __utmc=30149280; __utmz=30149280.1534912220.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ps=y; dbcl2="148093400:P2npGQhCpGg"; ck=2A7G; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=D8A4EBBD11D9AA57DAD703B8C832E64FF|d61325b8810b5ba648a4e960d3d4d730; frodotk="355bfb16e58409faa013f144b08c1dee"; talionusr="eyJpZCI6ICIxNDgwOTM0MDAiLCAibmFtZSI6ICJcdTY3MzFcdTY2NTcifQ=="; __guid=52291701.2921635455745689600.1534915892185.5583; _ga=GA1.3.106230672.1534912220; _gid=GA1.3.1933977497.1534915893; monitor_count=4; Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1534915893,1534915902,1534915904,1534915913; Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2=1534915913'

class GetMvInfo(object):

    def __init__(self):
        self.headers={
             "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
        with requests.session() as s:
            self.s=s

    def get_cookies(self,method=None):
        if method=="search":
            cookie_str=cookie_str_former
        else:
            cookie_str='ll="118254"; bid=MKV-C3S5_Dk; __utmc=30149280; ps=y; dbcl2="148093400:P2npGQhCpGg"; ck=2A7G; __guid=223695111.248253277858958820.1534912238606.3452; __utmc=223695111; __yadk_uid=Yl5fQFI4fIzcCbutj9lVsOrfyd5wDDwj; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=D8A4EBBD11D9AA57DAD703B8C832E64FF|d61325b8810b5ba648a4e960d3d4d730; monitor_count=2; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1534916314%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=0d20c3633a0b89c5.1534912240.2.1534916314.1534912251.; _pk_ses.100001.4cf6=*; __utma=30149280.106230672.1534912220.1534912220.1534916314.2; __utmb=30149280.0.10.1534916314; __utmz=30149280.1534916314.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1555391677.1534912240.1534912240.1534916314.2; __utmb=223695111.0.10.1534916314; __utmz=223695111.1534916314.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; report=ref=%2F&from=mv_a_tl'
        return {key.strip().split("=", 1)[0]: key.strip().split("=", 1)[1] \
                        for key in cookie_str.strip().split(";")}

    def html_response(self,url,method=None):
        try:
            page_content = requests.get(url).text
        except RequestException as e:
            print("Err:", e.args)
            return None
        regex=r"检测到有异常请求"
        cookies=self.get_cookies(method)
        if re.search(regex,page_content.strip()):
            page_content=self.s.get(url,headers=self.headers,cookies=cookies).text
        return BeautifulSoup(page_content, "html.parser")

    def getMovieTopic(self,SearchTopic):
        base_url = "https://m.douban.com/search/?query={}&type=movie".format(quote(SearchTopic))
        page_content=self.html_response(base_url,method="search")
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
            item = page_content.find("div", {"id": "info"}).stripped_strings
            for string in item:
                if string in ["编剧", "主演", "类型:", "制片国家/地区:", \
                              "语言:", "上映日期:", "片长:", "又名:", "IMDb链接:"]:
                    string = "\n" + string
                movie_info.append(string)
            return "".join(movie_info)
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

    def get_basic_info(self,url):
        page_content = self.html_response(url)
        info,summary=self.getMovieInfo(page_content),self.getShortSummary(page_content)
        return info,summary

    def close_session(self):
        self.s.close()

# t=GetMvInfo().get_basic_info("https://movie.douban.com/subject/25966209/")
# print(t)
