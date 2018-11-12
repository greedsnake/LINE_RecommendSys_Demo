# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 00:17:32 2018

@author: linzino
"""
import requests #引入函式庫
from bs4 import BeautifulSoup
import re
import json
import feedparser

def google(message):
    '''
    抓到最新google map資料
    '''
    pretext = ')]}\''
    
    # 爬下com南港分行
    url=['https://www.google.com.tw/maps/preview/reviews?authuser=0&hl=zh-TW&gl=tw&pb=!1s0x3442ab5ed8270bf5%3A0xca5639af83a88adc!2i0!3i10!4e3!7m4!2b1!3b1!5b1!6b1',
        'https://www.google.com.tw/maps/preview/reviews?authuser=0&hl=zh-TW&gl=tw&pb=!1s0x3442acbde079d169%3A0x8810bd0a963d1727!2i0!3i10!4e3!7m4!2b1!3b1!5b1!6b1']
	 
    bn=[120,142]
    i=bn.index(message)
    resp = requests.get(url[i])
    text = resp.text.replace(pretext,'')
    soup = json.loads(text)
    
    # 抓第一篇
    first = soup[0][0]
    # 整理資料 
    username = first[0][1]
    time = first[1]
    mesg = first[3]
    star = first[4]
    
    string = '%s \n於 %s 將您評為 %s顆星 \n留言：%s' % (username, time,star,mesg)

    
    return string
