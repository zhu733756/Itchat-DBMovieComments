# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
from pyecharts import Geo,Style,Pie
from pymongo import MongoClient
from collections import Counter
import re,os,bisect,itertools
from functools import reduce
from jieba import analyse
import matplotlib.pyplot as plt
from GetMovieInfo import GetMvInfo
from wordcloud import STOPWORDS, ImageColorGenerator

class MongoAnalysis(object):

    def __init__(self,tbname=None,saved_file_type=None):

        if tbname is None:
            raise ValueError("Not get a tbname!")
        self.tbname = tbname
        self.conn= MongoClient("localhost:27017", connect=True)
        self.db = self.conn['DBMovie']
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

    def get_title(self):
        '''
        get the title of the movie
        :return:
        '''
        search_number=re.compile(r"\d+").findall(self.tbname)[0]
        title=GetMvInfo().get_title(search_number)
        if not title:
            title=self.tbname
        return title

    def GetOneCol(self,name,method=None):
        '''
        give a name to search the column name in mongodb
        :param name: colname,such as "comment_content".
        :param method:
        if method is None,we should remove the null data.
        if method is 'average',we should fill the null data with the mean value.
        :return: nonempty set
        '''
        if method is None:
            return [comments[name].strip()
                      for comments in self.collection.find()
                      if comments[name] is not None]
        elif method == "average":
            com_lst=[comments[name].strip()
                     for comments in self.collection.find()
                     if comments[name] is not None]
            aver=reduce(lambda x,y:x+y,map(int,com_lst))/len(com_lst)
            result=[]
            for comments in self.collection.find():
                if comments[name]:
                    result.append(int(comments[name].strip()))
                else:
                    result.append(aver)
            return result

    def AreaMap(self):
        '''
        :return: a area map on chinese map
        downloaded maps:
        pip install echarts-countries-pypkg
        pip install echarts-china-provinces-pypkg
        pip install echarts-china-cities-pypkg
        pip install echarts-china-counties-pypkg
        pip install echarts-china-misc-pypkg
        pip install echarts-china-kingdom-pypkg
        '''
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
        v_max=max(v_lst)
        geo=Geo(self.get_title(),"数据来源：豆瓣电影",**self.style.init_style)
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

    def GetStars(self,star_score):
        '''
        search for grades with star_score
        :param star_score: int
        :return: a list of grades
        '''
        breakpoints = [11, 21, 31, 41, 51]
        grades=["一星","二星","三星","四星","五星"]
        return grades[bisect.bisect(breakpoints,star_score)]

    def StarMap(self):
        '''
        Get a pie map
        :return:
        '''
        score=dict(Counter(map(self.GetStars,
                               self.GetOneCol(name="comment_score",method="average"))))
        attr,value=Geo.cast(score)
        pie=Pie(self.get_title(),"数据来源：豆瓣电影",title_pos="center",width=900)
        pie.add("",attr,value,center=[50,50],is_random=True,
                radius=[30,75],rosetype="area",
                is_legend_show=False,is_label_show=True)
        if self.saved_file_type is None:
            pie.render(os.path.join(self.path,"StarMap.png"))
        elif self.saved_file_type=="html":
            pie.render(os.path.join(self.path,"StarMap.html"))

    def Cast(self,name,method=None,message=None,max_bin=100):
        '''
        casts data ,and filters data with stopwords
        :param name: colname
        :param method: to decide the func returns a dict or tuple(attr,value)
        :param message: a message the user gives,if not None, will be adding to stopwords
        :param max_bin: the max number of words on wordcloud
        :return:
        '''
        string = "".join(self.GetOneCol(name))
        brokewords=map(str.strip,
                       open('./config/stopwords/stopwords.txt', "r", encoding="utf-8")
                       .readlines())
        if message:
            brokewords=itertools.chain(brokewords,message.split(",")[:])
        stopwords = "".join(brokewords)
        lis = dict(Counter([tag.strip()
                        for tag in analyse.extract_tags(string, max_bin)
                        if tag.strip() not in stopwords]))
        lis = sorted(lis.items(), key=lambda x: x[1], reverse=True)
        if method is None:
            return Geo.cast(lis)
        elif method=="dict":
            return {k[0]:k[1] for k in lis}

    def WordCloudMap(self,message=None):
        '''
        a high-class wordcloud
        :param message: messages that user gives
        :return:
        '''
        from wordcloud import WordCloud
        backgroud_path = './img/{}/background/{}.png'.format(self.tbname, self.tbname)
        if not os.path.exists(backgroud_path):
            backgroud_path = './img/sample/1.jpg'
        backgroud_image = plt.imread(backgroud_path)
        cloud = WordCloud(
            width=1024, height=768,
            font_path='./config/fonts/simhei.ttf',
            background_color='white',  # 设置背景色
            mask=backgroud_image,  # 词云形状False
            max_words=100,  # 允许最大词汇
            max_font_size=400,  # 最大号字体
            random_state=50  # 旋转角度
        )
        if message is None:
            text=self.Cast(name="comment_content",method="dict")
        else:
            message.replace("，",",")
            if "," not in message:
                message=message+","
            text = self.Cast(name="comment_content", method="dict",message=message)
        cloud.fit_words(text)  # 产生词云
        cloud.recolor(color_func=ImageColorGenerator(backgroud_image))
        plt.figure()
        plt.imshow(cloud)
        plt.axis('off')
        cloud.to_file(os.path.join(self.path, "wordcloud.png"))

    def SimpleWordCloudMap(self):
        '''
        a lower-class wordcloud
        :return:
        '''
        from pyecharts.charts.wordcloud import WordCloud
        attr,value=self.Cast(name="comment_content")
        wordcloud = WordCloud(self.get_title(),"数据来源：豆瓣电影",title_pos="center",width=1200, height=600)
        wordcloud.add("", attr, value, shape="diamond",word_size_range=[20, 100])
        if self.saved_file_type is None:
            wordcloud.render(os.path.join(self.path,"wordcloud.png"))
        elif self.saved_file_type=="html":
            wordcloud.render(os.path.join(self.path,"wordcloud.html"))

    def close(self):
        self.conn.close()

# m=MongoAnalysis(tbname="comments_25966209")
# m.StarMap()
# m.AreaMap()
# m.SimpleWordCloudMap()
# m.close()
