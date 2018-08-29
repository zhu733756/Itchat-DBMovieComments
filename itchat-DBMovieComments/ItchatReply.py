# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
from ItchatRoom import ItchatRoom
import itchat
from GetMovieInfo import GetMvInfo
from collections import deque
from MongoAnalysis import MongoAnalysis

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
                    "友情提示：如果小主想要退出本系统继续聊天，请输入chat；\n"
                    "关闭聊天系统，请输入Esc。", fromName)
        user_info["flag"]=1
        user_info["deque"]=deque(["kw"],maxlen=2)
        itchat.send("现在已经进入系统，请输入关键词：", fromName)

def start_crawl(url,toName):
    self.redis.lpush("douban_spider:start_urls", url)
    itchat.send("Your desired movie is now under crawling,please wait it ends... ", toName)
    itchat.send("lpush douban_spider:start_urls %s" % url, "filehelper")

def get_tbname():
    pass

def saved_user_info():
    return {}.setdefault(tbname,[]).append(toName)

def end_crawl():
    pass

def send_MongoAnalysis():
    info=saved_user_info()
    if tbname is completed:
        m = MongoAnalysis(tbname=tbname)
        m.AreaMap()
        m.StarMap()
        m.SimpleWordCloud()
        m.close()
        for user in info[tbname]:
            itchat.send("给你要的数据分析~~~",toUserName=user)

def schedule():
    pass


