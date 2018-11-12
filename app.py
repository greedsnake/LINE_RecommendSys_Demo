# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 18:12:45 2018

@author: linzino
"""

from linebot.models import *
from datetime import datetime 
import feedparser
import random
# line-bot
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# mongodb
from pymongo import MongoClient
import pymongo
import urllib.parse
from datetime import datetime 

# server-side
from flask import Flask, request, abort

# line-bot
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# package
import re
from datetime import datetime 

# customer module
import mongodb
import corwler


app = Flask(__name__)

line_bot_api = LineBotApi('tALJGyw5Gzes13Eo59pE+eRR5fV11Dw6SYCshuxGkwjaMr+PEI+EeKY9YzoUyERZIccZqD4zTt4LKtYkVQINT1eOEgZaPtAReN+Oc2V8hsmbNgNsw+SnQDuqDLo8EzR1+7ID/7KkCNCbmMURnvxhQQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ee211365f9ec399943c478989fe2eed5')

msg1 = ""
msg2 = ""
msg3 = ""


@app.route("/callback", methods=['POST'])

def callback():
    
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    '''
    當使用者加入時觸動
    '''
    # 取得使用者資料
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    
    print(name)
    print(uid)
    # Udbddac07bac1811e17ffbbd9db459079
    if mongodb.find_user(uid,'users')<= 0:
        # 整理資料
        dic = {'userid':uid,
               'username':name,
               'creattime':datetime.now(),
               'Note':'user',
               'ready':0}
        
        mongodb.insert_one(dic,'users')

@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):

    '''
    當收到使用者訊息的時候
    '''
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    message = event.message.text 
           
    def choose_id():
      # 設定使用者下一句話要群廣播
      mongodb.update_byid(uid,{'ready':1},'users')
      global msg1
      msg1 = 1
      remessage = TextSendMessage(text='請輸入客戶編號')
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      
    def get_id(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg1
      msg1 = message
      
    def choose_age():
      # 設定使用者下一句話要群廣播
      mongodb.update_byid(uid,{'ready':1},'users')
      global msg2
      msg2 = 1
      remessage = TextSendMessage(text='請輸入客戶年齡')
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
           
    def get_age(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg2
      msg2 = message
    
    def choose_gender():
      # 設定使用者下一句話要群廣播
      mongodb.update_byid(uid,{'ready':1},'users')
      global msg3
      msg3 = 1
      remessage = TextSendMessage(text='請輸入客戶性別(0:女性; 1:男性)')
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      
    def get_gender(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg3
      msg3 = message
      
    def clear():
      global msg1,msg2,msg3
      msg1 = ""
      msg2 = ""
      msg3 = ""
      remessage = TextSendMessage(text='已清除輸入資料')
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      
    def suggest(message,msg3):
      if msg3==0:
          sex="女性"
      elif msg3==1:
          sex="男性"
      else:
          sex="未知"
      remessage = TextSendMessage(text='查詢顧客ID=%s;年齡=%s; 性別=%s 的推薦商品:' % (str(msg1), str(msg2), sex) )
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      text = report(msg1,msg2,msg3)
      # 包裝訊息
      remessage2 = TextSendMessage(text=text)
      # 回應使用者
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage2)      
    
    def report(x,y,z):        
        string = '誠心推薦!!%s, %s, %s' % (str(x),str(y),str(z))
        return string
      
    if message == 'ID':
        choose_id()
        
    if message == '年齡':
        choose_age()
    
    if message == '性別':
        choose_gender()
    
    if message == '清除':
        clear()
    
    if message == '推薦':
        suggest(message,msg3)
    
    if mongodb.get_ready(uid,'users') ==1 and msg1==1:
        get_id(message)        
    
    if mongodb.get_ready(uid,'users') ==1 and msg2==1:
        get_age(message)
    
    if mongodb.get_ready(uid,'users') ==1 and msg3==1:
        get_gender(message)
    """
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    """
    return 0 


if __name__ == '__main__':
    app.run(debug=True)