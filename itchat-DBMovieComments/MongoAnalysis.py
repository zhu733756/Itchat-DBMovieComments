# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""

from MovieComments import settings
from pyecharts import Geo,Style
from pymongo import MongoClient
from collections import Counter
import pandas as pd
import re,os,bisect
from functools import reduce
from jieba import analyse,cut
import matplotlib.pyplot as plt

class MongoAnalysis(object):

    def __init__(self,tbname=None,saved_file_type=None):

        if tbname is None:
            raise ValueError("Not get a tbname!")
        self.tbname = tbname
        self.db = MongoClient("localhost:27017", connect=True)['DBMovie']
        self.collection = self.db[self.tbname]
        self.style=Style(title_color='#fff',
                         title_pos="center",
                         width=1200,
                         height=600,
                         background_color='#404a59')
        self.saved_file_type=saved_file_type
        self.path='./img/{}/finished'.format(self.tbname)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def GetOneCol(self,name,method=None):

        if method is None:
            return [comments[name]
                      for comments in self.collection.find()
                      if comments[name] is not None]
        elif method == "average":
            com_lst=[comments[name]
                     for comments in self.collection.find()
                     if comments[name] is not None]
            aver=reduce(lambda x,y:x+y,com_lst)/len(com_lst)
            result=[]
            for comments in self.collection.find():
                if comments[name] is None:
                    result.append(aver)
                result.append(comments[name])

    def GetStars(self,star_score, breakpoints=[0, 10, 20, 30, 40, 50]):
        grades=["一星","二星","三星","四星","五星"]
        return grades[bisect.bisect(breackpoints,star_score)]

    def AreaMap(self,title=None):
        '''
        :param title: title of area map
        :return: a area map on chinese map
        downloaded maps:
        pip install echarts-countries-pypkg
        pip install echarts-china-provinces-pypkg
        pip install echarts-china-cities-pypkg
        pip install echarts-china-counties-pypkg
        pip install echarts-china-misc-pypkg
        pip install echarts-china-kingdom-pypkg
        '''
        if title is None:
            title = self.tbname
        # filter other countries' users
        city=dict(Counter(self.GetOneCol(name="city")))
        filter_city={key:city[key]
                     for key in city.keys()
                     if re.compile(r'[\u4e00-\u9fa5]+').search(key[0])}
        key_map=[
            "河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建"
            ,"江西","山东","河南","湖北","湖南","广东","海南","四川","贵州",
            "云南","陕西","甘肃","青海","台湾"
        ]
        k_lst,v_lst=[],[]
        for key in sorted(list(filter_city.keys())):
            v_lst.append(filter_city[key])
            if "," in key:
                key=key.split(",")[0].strip()
            for province in key_map:
                if province in key:
                    key=key.replace(province,"").strip()
            k_lst.append(key)
        print(k_lst,v_lst)
        v_max=max(v_lst)
        geo=Geo(title,"数据来源：豆瓣电影",**self.style.init_style)
        geo.add("",k_lst,v_lst,
                type='effectScatter',#other styles:scatter or heatmap
                visual_range=[0,v_max],
                visual_range_text="#fff",
                symbol_size=15,
                is_visualmap=True)
        if self.saved_file_type is None:
            geo.render(os.path.join(self.path,"AreaMap.png"))
        elif self.saved_file_type=="html":
            geo.render(os.path.join(self.path,"AreaMap.html"))

    def StarMap(self):
        pass

    def WorldCloudMap(self,message=None,max_bin=100):
        if message is None:
            print("No stopwords!")
            self.SimpleWorldCloudMap()
        elif "," not in message:
            raise ValueError('屏蔽词请以，隔开')
        else:
            from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
            string="".join(self.GetOneCol(name="comment_content"))
            lis="".join(cut(string, cut_all=False))
            backgroud_path='./img/{}/background/{}.png'.format(self.tbname,self.tbname)
            if not os.path.exists(backgroud_path):
                backgroud_path ='./img/sample/1.jpg'
            backgroud_image=plt.imread(backgroud_path)
            stopwords=STOPWORDS.copy()
            for mes in message.split(","):
                stopwords.add(mes)
            cloud = WordCloud(
                width=1024,height=768,
                font_path='./fonts/simhei.ttf',
                background_color='white',# 设置背景色
                mask=backgroud_image,# 词云形状
                max_words=100,# 允许最大词汇
                max_font_size=400,# 最大号字体
                random_state=50#旋转角度
            )
            word_cloud = cloud.generate(lis)  # 产生词云
            img_colors=ImageColorGenerator(backgroud_image)
            word_cloud.recolor(color_func=img_colors)
            plt.imshow(word_cloud)
            plt.axis('off')
            plt.show()
            word_cloud.to_file(os.path.join(self.path,"worldcloud_3.png"))

    def SimpleWorldCloudMap(self,max_bin=100):
        from pyecharts.charts.wordcloud import WordCloud
        string = "".join(self.GetOneCol(name="comment_content"))
        lis = Counter([tag for tag in cut(string, cut_all=False)])
        attr, value = [], []
        for i in analyse.extract_tags(string, max_bin):
            if i in lis:
                attr.append(i)
                value.append(lis[i])
        wordcloud = WordCloud(width=1200, height=600)
        wordcloud.add("", attr, value, word_size_range=[20, 100])
        if self.saved_file_type is None:
            wordcloud.render(os.path.join(self.path,"worldcloud.png"))
        elif self.saved_file_type=="html":
            wordcloud.render(os.path.join(self.path,"worldcloud.html"))

MongoAnalysis(tbname="comments_26872492").WorldCloudMap(message="不能,什么,自己")