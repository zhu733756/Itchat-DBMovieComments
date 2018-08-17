# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
import itchat
import requests
from GetMobSubject import getMovieTopic
from GetMovieInfo import *
from collections import deque

class ItchatRoom(object):

    def __init__(self):
        self._flag=0
        self.topicUrls={}
        self.deque=deque(["kw"],maxlen=2)

    @classmethod
    def getResponse(self,msg):
        api= 'http://www.tuling123.com/openapi/api'
        data = {
            'key': '7c1ccc2786df4e1685dda9f7a98c4ec9',
            'info': msg,
            'userid': 'wechat-robot',
        }
        r = requests.post(api, data=data).json()
        return r["text"] or msg

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self,flag):
        self._flag=flag

    def get_nextAction(self,text,toName):
        print("----")
        print(self.deque)
        print(self.topicUrls)
        print("-------")
        if self.deque[0] == "kw" and text != "back":
            self.get_keywords(text,toName)
            self.deque.appendleft("info")
        if text.isdigit():
            self.get_info(text,toName)
            self.deque.appendleft("crawl "+self.get_crawlUrl(text))
        if text == "back":
            itchat.send("请重新输入关键词：",toName)
            self.deque.appendleft("kw")
            self.topicUrls.clear()
        if text=="crawl" and text in self.deque[0]:
            itchat.send("Start crawl url: "+self.deque[0].split()[1],toName)

    def get_keywords(self,text,toName):
        movie_topic = getMovieTopic(text.strip())
        movieList = json.loads(movie_topic)
        item = []
        for movieDic in movieList:
            item.append(", ".join(list(movieDic.values())[:-1]))
            self.topicUrls.setdefault(movieDic["No"], movieDic["href"])
        itchat.send("匹配详情(No.,title,score)如下:\n" + "\n".join(item), toName)

    def get_info(self,text,toName):
        if self.topicUrls:
            if text not in self.topicUrls:
                itchat.send("好像没有这个数值选项！",toName)
            url = self.topicUrls[text]
            t = html_response(url)
            itchat.send("电影阵容：\n"+getMovieInfo(t),toName)
            itchat.send("内容简介：\n"+getShortSummary(t),toName)
        else:
            itchat.send("请求出错！")

    def get_crawlUrl(self,text):
        if self.topicUrls and self.topicUrls[text]:
            url = self.topicUrls[text]+"comments"
            return url
        else:
            itchat.send("请求出错！")

    def get_tuling_reply(self,text,toName):
        itchat.send(self.getResponse(text),toName)


itchat_room=ItchatRoom()

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    text = msg["Text"].strip()
    fromName=msg["FromUserName"]
    toName = msg["ToUserName"]
    print(toName,fromName)
    print("-----------")
    if text in ("Esc", "ESC", "esc"):
        itchat.send("拜拜小主人~~~",fromName)
        itchat.logout()
    if text=="chat":
        ItchatRoom.flag=0
    if itchat_room.flag:
        itchat_room.get_nextAction(text,fromName)
    else:
        itchat_room.get_tuling_reply(text,fromName)
    if text in ("电影", "mv", "movie", "豆瓣") and not itchat_room.flag:
        itchat.send("终于等到你,还好没放弃~~~"
                    "小可耐是不是迫不及待地想查看豆瓣电影分析？\n"
                    "官人别急，查询电影，请输入电影关键词：例如，钢铁侠\n"
                    "友情提示：如果小主想要退出本系统继续聊天，请输入chat；关闭聊天系统，请输入Esc。", fromName)
        itchat.send("现在已经进入系统，请输入关键词：", fromName)
        itchat_room.flag = 1

if __name__ == "__main__":

    itchat.auto_login()
    itchat.run()



