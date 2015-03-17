#!/usr/bin/env python
#coding=utf-8
import sys
import os
sys.path.append("./jieba")
import jieba
import jieba.analyse
import json
import sys
import datetime
import time
import re
from os import listdir
from os.path import isfile, join

#設定字典
jieba.set_dictionary('extra_dict/dict.txt.big')
#檢查使用者自訂字典是否存在
if os.path.isfile("result/dict/custom_word.wd"):
    jieba.load_userdict("result/dict/custom_word.wd")

mypath = "./datatmp/2015_03_01/"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
date = "2015_03_01"
for f in onlyfiles:
	content = open(os.path.join(mypath,f), "r").read()
	words = jieba.analyse.extract_tags_custom(content, topK=10,detectedwdsavepath='result/newwd/' + date + ".wd")
	print ", ".join(words)