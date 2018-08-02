# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""

import xlrd,xlwt,os,datetime,re,shutil
from multiprocessing import Pool,Process

class kill(object):
    def __init__(self,filename=None,titles=None):

        self.index=0
        self.filename=filename
        self.id=[]
        self.titles=titles

    def get_number(self,number):
        if number:
            for i in range(number):
                number_index=i+1
                name="name"+str(number_index)
                setattr(self,name,[])
        else:
            print("invalid number!")

    def open_xls(self):
        workbook = xlrd.open_workbook(self.filename)
        sheet1=workbook.sheet_by_name("Sheet1")
        return sheet1

    def get_whole_identification(self):
        col1=self.open_xls().col_values(2)#第三列
        for i in col1:
            if  "ppm" not in i.strip() and i and i !="kb":
                self.id.append(i.strip())

    def get_name_vaule(self):
        number = len(self.titles) - 1
        self.get_number(number)
        first_id = self.titles[1].split(" ")[0]
        print(" Found first:",first_id)
        name_id = self.open_xls().col_values(0)
        for x,y in enumerate(name_id):
            for i in range(number):
                if y.strip().split(" ")[0]==first_id:
                    val=self.open_xls().cell(x+i,27).value
                    name="name"+str(i+1)
                    if val:
                        getattr(self,name).append(val)

class put_values(object):

    def __init__(self,filename=None):
        self.filename=filename
        self.newfilename=None

    @classmethod
    def get_Date(cls):
        now = datetime.datetime.now().date()
        return str(now).replace("-","")

    def get_path(self):

        temp = self.filename.split(" ")
        self.newfilename = temp[0] + " " + temp[2]
        path="E:\dataraw\%s"%(self.get_Date())
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def print_vaual(self,xx):

        p = kill(filename=self.filename,titles=xx)
        number=len(p.titles)-1
        p.get_whole_identification()
        p.get_name_vaule()
        f=xlwt.Workbook()
        sheet = f.add_sheet(sheetname="data", cell_overwrite_ok=True)
        for num,title in enumerate(p.titles):
            sheet.write(0,num,title)
        for num,id in enumerate(p.id):
            sheet.write(num+1,0,id)
        for i in range(number):
            name = "name" + str(i + 1)
            for num,ns in enumerate(getattr(p,name)):
                sheet.write(num+1, i+1, ns)
        fpath=self.get_path()+"\\"+self.newfilename
        f.save(fpath)
        print("saved a dir for %s" %fpath)
        srcdir=os.path.dirname(os.path.abspath("__filename__"))+"\\"+self.filename
        stdir=self.get_path()+"\\"+self.filename
        shutil.move(srcdir,stdir)
        print("%s move to %s"%(srcdir,stdir))

def mapping(**kwargs):

    key={}

    filelist={files.split("-")[1]:files for files in os.listdir(".") if "icpoes" in files.lower()}

    for k,v in kwargs.items():

        item = ["Sample"]
        if k not in filelist:
            continue
        filename = filelist[k]
        if isinstance(v, list):
            for vi in v:
                item.extend([vi + " mg/L"])
            key[filename] = item
        if isinstance(v, str):
            for vi in v.split(" "):
                item.extend([vi+ " mg/L"])
            key[filename] = item

    return key

if __name__=="__main__":
    dic={"gefeng":["Mg","K","Ca","Na"],"wuzhenbin":["Mg", "K", "Ca", "Na"],"zhangxuezhi":["Al"],"liangwei":["Mg","K","Ca","Na","Al","Fe"],"wuda":["Mg","K","Ca","Na","Al","Fe","Li","Ti"]}
    key=mapping(**dic)
    print(key)
    for k,v in key.items():
        pro=Process(target=put_values(k).print_vaual,args=(v,))
        pro.start()
        pro.join()

