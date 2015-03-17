#!/usr/bin/env python
#coding=utf-8
import sys
import os
sys.path.append("./jieba")
import jieba
import jieba.analyse
import json
import sys
import pymongo
from pymongo import MongoClient
import datetime
import time
from bson import json_util
from bson import BSON
import re


def cleanhtmlcode(contain):
  contain = re.sub(r'<a[\w\W]*?/a>', '  ', contain)
  contain = re.sub(r'<span[\w\W]*?/span>', '', contain)
  contain = re.sub(r'<div[\w\W]*?/div>', '', contain)
  return contain

def list_encode(words):
  wlist = []
  for w in words:
    if isinstance(w, unicode):
      wlist.append(w.encode("utf-8"))
    else:
      wlist.append(w)
  return wlist

jieba.set_dictionary('extra_dict/dict.txt.big')
if os.path.isfile("result/dict/custom_word.wd"):
    jieba.load_userdict("result/dict/custom_word.wd")



contain = """
慈濟宇宙大覺者　換成魯夫、悟空你買不買？ http://goo.gl/wV8ZZR 水果 慈濟販售要價33萬元的「宇宙大覺者」雕像近日引發外界議論。有網友在網路上用電腦修 圖，把「宇宙大覺者」雕像改成卡通人物魯夫、悟空、河馬、雅典娜等，在網路被瘋傳， 許多網友稱讚「超想要」、「拿到動漫展去賣絕對會創業績紀錄」！ 批踢踢網友a71195今天在批踢踢joke板貼文，「分享強者我朋友做的大覺者系列」，把原 先慈濟的「宇宙大覺者」中，佛陀人像改成包括《航海王》主角魯夫、《辛普森家庭》主 角河馬等動漫人物。有網友回應：「同樣33萬我寧願買雅典娜」、「靠，好讚，好想買XD 」。（生活中心／台北報導） http://i.imgur.com/7mexIrF.jpg
網友把慈濟的宇宙大覺者雕像換成航海王主角魯夫。翻攝自網路 http://i.imgur.com/Zy2IWmM.jpg
網友把慈濟的宇宙大覺者雕像換成七龍珠主角孫悟空。翻攝自網路 http://i.imgur.com/URYItvL.jpg
網友把慈濟的宇宙大覺者雕像換成辛普森家庭主角河馬。翻攝自網路 http://i.imgur.com/vHShTev.jpg
網友把慈濟的宇宙大覺者雕像換成聖鬥士主角紫龍。翻攝自網路 http://i.imgur.com/svcrvXS.jpg
網友把慈濟的宇宙大覺者雕像換成聖鬥士主角雅典娜。翻攝自網路
"""
words = jieba.analyse.extract_tags_custom(contain, topK=10,detectedwdsavepath="result/newwd/tests.wd")
words = list_encode(words)
try:
  #insert result into mongodb
  #outcoll.insert(post)
  #indent=4
  for w in words:
    print w
except pymongo.errors.DuplicateKeyError:
  print 'alreay had key, skip it'
