# [itchat-DBMovieComments图文说明]

## 功能介绍：
#### 本project不仅是一个能和图灵机器人聊天的程序（这一部分不作说明了），而且还添加了彩蛋，能实时获取豆瓣影评，自动生成可视化数据发送给用户。

## 使用说明：
#### 确认开发环境搭配好后，我们可以使用微信操作：
#### 1 开启彩蛋(彩蛋关键词主要有：豆瓣、电影、movie等)
![python](https://github.com/zhu733756/WebSpider/blob/spiders/source/1.png)
#### 2 搜索电影名称（继续输入电影名称或者需要搜索的关键词，比如我这里输入1）
![python](https://github.com/zhu733756/WebSpider/blob/spiders/source/2.png)
#### 3 选择电影序号，查看电影简介（输入数字即可，一般来说，不超过10，但也不要输入0，这里我选择3，选中第三部电影，显示结果就是电影简介）
![python](https://github.com/zhu733756/WebSpider/blob/spiders/source/3.png)
#### 4 确认选择，就输入crawl，这样就能自动加入下载队列了，当然如果不是你想要的电影，可以选择back返回上一级，重新输入
![python](https://github.com/zhu733756/WebSpider/blob/spiders/source/5.png)
#### 5 如果有第二个需求，输入back返回上一级重新输入，重复第三步或者第四步
![python](https://github.com/zhu733756/WebSpider/blob/spiders/source/4.png)
#### 6 爬取过程中，可以随时输入chat进入聊天，或者esc退出程序
#### 7 等到爬虫爬取完毕后（需要等待一段时间），会把结果发给用户
![python](https://github.com/zhu733756/WebSpider/blob/spiders/source/6.png)

## 依赖安装
'''
pip install -r requirements.txt
'''

## 开发环境
#### windows 7, python 3.6(作者下载的是对应python3.6版本的anconda)

## 打开数据库连接（redis和mongo）
#### 在pycharm中运行start.bat
![python](https://github.com/zhu733756/WebSpider/blob/spiders/source/7.png)

## 配置代理池(确认redis数据库已经打开)
#### 进入proxypool目录，修改settings.py文件
#### PASSWORD为Redis密码，如果为空，则设置为None
#### python run.py

## 最后：
#### WebSpider文件夹中包含两个project
#### itchat-DBMovieComment以及ProxyPool-master(这个project来自崔大大@Germey，感谢他，不用让作者再造轮子！)。
#### 前者也就是主程序，后者是代理抓取程序，缺一不可。
