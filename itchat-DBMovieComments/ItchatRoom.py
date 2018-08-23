# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
import itchat
import requests,json
from GetMovieInfo import GetMvInfo
from collections import deque
from scrapy import cmdline
from redis import StrictRedis,ConnectionPool

class ItchatRoom(object):

    def __init__(self):
        self._flag=0
        self.topicUrls={}#用来采集爬取的关键词信息
        self.dequelist={}#用来储存用户信息
        self.redis=StrictRedis(connection_pool=ConnectionPool(host="localhost",port=6379))

    @classmethod
    def getResponse(self,msg):
        '''
        返回图灵机器人对话内容
        :param msg: 用户输入的文本
        :return:
        '''
        api= 'http://www.tuling123.com/openapi/api'
        data = {
            'key': '7c1ccc2786df4e1685dda9f7a98c4ec9',#注册图灵机器人得到的key
            'info': msg,
            'userid': 'wechat-robot',
        }
        r = requests.post(api, data=data).json()
        return r["text"] or msg

    def get_nextAction(self,text,toName,user_deque):
        '''
        执行下一步操作
        :param text:用户输入的文本
        :param toName: 发送指令的用户名，需要返回的用户名
        :return:
        '''
        print("----")
        print(user_deque)
        print(self.topicUrls)
        print("-------")
        if user_deque[0] == "kw" and text != "back":
            self.get_keywords(text,toName)
            user_deque.appendleft("info")
            if text.isdigit():#防止第一次输入数字导致没有经过用户选择就直接进入下一步
                text = text+"_salt"
        if text.isdigit() and user_deque[0] == "info":
            try:
                self.get_info(text,toName)
            except KeyError:
                itchat.send("好像没有这个数值选项！支持的数值选项：1-{}".format(self.topicUrls), toName)
            if text in self.topicUrls:
                user_deque.appendleft("crawl "+self.get_crawlUrl(text))
        if text == "back":
            itchat.send("请重新输入关键词：",toName)
            user_deque.appendleft("kw")
            self.topicUrls.clear()
        if text=="crawl" and text in user_deque[0]:
            url=user_deque[0].split()[1]
            itchat.send("Start crawl url: "+url,toName)
            self.redis.lpush("douban_spider:start_urls",url)
            itchat.send("lpush douban_spider:start_urls %s" % url, "filehelper")

    def get_keywords(self,text,toName):
        '''
        用来返回指定关键词的最佳搜索结果
        :param text: 用户输入文本
        :param toName: 需要返回的用户名
        :return:
        '''
        movie_topic = get_movie_info.getMovieTopic(text)
        print(movie_topic)
        movieList = json.loads(movie_topic)
        item = []
        for movieDic in movieList:
            item.append(",".join(list(movieDic.values())[:-1]))
            self.topicUrls.setdefault(movieDic["No"], movieDic["href"])
        itchat.send("匹配详情(No.,title,score)如下:\n" + "\n".join(item), toName)

    def get_info(self,text,toName):
        '''
        用来返回搜索详情
        :param text: 输入指令，要求为digit
        :param toName: 需要返回的用户名
        :return:
        '''
        if self.topicUrls:
            url = self.topicUrls[text]
            info,summary=get_movie_info.getMovieInfo(url),get_movie_info.getShortSummary(url)
            itchat.send("电影阵容：\n"+info,toName)
            itchat.send("内容简介：\n"+summary,toName)
        else:
            itchat.send("请求出错！",toName)

    def get_crawlUrl(self,text):
        '''
        用来捕获用户需要抓取的url
        :param text: 需要返回的用户名
        :return:
        '''
        if self.topicUrls and self.topicUrls[text]:
            url = self.topicUrls[text]+"comments"
            return url
        else:
            itchat.send("请求出错！",toName)

    def get_tuling_reply(self,text,toName):
        itchat.send(self.getResponse(text),toName)

itchat_room=ItchatRoom()
get_movie_info=GetMvInfo()

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    text = msg["Text"].strip()
    fromName=msg["FromUserName"]
    toName = msg["ToUserName"]
    print(fromName,toName)
    print("-----------")
    user_info = itchat_room.dequelist.setdefault(fromName, {})
    user_info.setdefault("deque", deque(["kw"], maxlen=2))
    user_info.setdefault("flag",0)
    if text in ("Esc", "ESC", "esc"):
        itchat.send("拜拜小主人~~~",fromName)
        get_movie_info.close_session()
        user_info["flag"]=0
        if toName == "filehelper":
            itchat.logout()
    if text=="chat":
        user_info["flag"]=0
    if user_info["flag"]:
        itchat_room.get_nextAction(text,fromName,user_info["deque"])
    else:
        itchat_room.get_tuling_reply(text,fromName)
    if text in ("电影", "mv", "movie", "豆瓣") and not user_info["flag"]:
        itchat.send("终于等到你,还好没放弃~~~"
                    "小可耐是不是迫不及待地想查看豆瓣电影分析？\n"
                    "官人别急，查询电影，请输入电影关键词：例如，钢铁侠\n"
                    "友情提示：如果小主想要退出本系统继续聊天，请输入chat；关闭聊天系统，请输入Esc。", fromName)
        user_info["flag"]=1
        user_info["deque"]=deque(["kw"],maxlen=2)
        itchat.send("现在已经进入系统，请输入关键词：", fromName)





