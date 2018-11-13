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

msg1 = msg2 = msg3 = ""
fmsg1 = fmsg2 = fmsg3 = 0

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
      global fmsg1
      fmsg1 = 1
      remessage = TextSendMessage(text='請輸入客戶編號')
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      
    def get_id(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg1,fmsg1
      fmsg1 = 0
      msg1 = message
      remessage = TextSendMessage(text='推薦客戶編號%s的商品:' % report1(msg1))
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      remessage2 = TextSendMessage(text = report1(msg1))
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage2)
      
    def choose_age():
      # 設定使用者下一句話要群廣播
      mongodb.update_byid(uid,{'ready':1},'users')
      global fmsg2
      fmsg2 = 1
      remessage = TextSendMessage(text="請輸入客戶年齡及性別(age,gender)\n女性請填'0',男性請填'1'")
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
           
    def get_age(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg2,fmsg2,cmd
      cmd = get_age(message)
      fmsg2 = 0
      msg2 = str.split(message)
      msg2 = tuple(msg2)
      if msg2[1]==0:
          sex='女性'
      elif msg2[1]==1:
          sex='男性'
      else:
          sex=''
      remessage = TextSendMessage(text='推薦%s歲%s客戶的商品:' % (msg2[0],sex))
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      remessage2 = TextSendMessage(text = report2(msg2))
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage2)
      
    def choose_gender():
      # 設定使用者下一句話要群廣播
      mongodb.update_byid(uid,{'ready':1},'users')
      global fmsg3
      fmsg3 = 1
      remessage = TextSendMessage(text='請輸入客戶性別(0:女性; 1:男性)')
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      
    def get_gender(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg3,fmsg3
      fmsg3 = 0
      msg3 = message
      rmsg3 = '顧客性別=' + msg3
      line_bot_api.reply_message(
                      event.reply_token,
                      rmsg3)
      
    def clear():
      global msg1,msg2,msg3
      global fmsg1,fmsg2,fmsg3
      msg1 = msg2 = msg3 = ""
      fmsg1 = fmsg2 = fmsg3 = 0
      remessage = TextSendMessage(text='已清除輸入資料')
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      
    def suggest(message,msg3):
      
      cid = msg1
      age = msg2
      if str(msg3)==str(0):
          sex="女性"
      elif str(msg3)==str(1):
          sex="男性"
      else:
          sex="未知"
      remessage = TextSendMessage(text='查詢顧客ID=%s; 年齡=%s; 性別=%s 的推薦商品:' % (str(cid), str(age), sex) )
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      text = report(cid,age,sex)
      datetime.time.sleep(2)
      # 包裝訊息
      remessage2 = TextSendMessage(text=text)
      # 回應使用者
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage2)
      
    
    def report1(cid):        
        string = '誠心推薦!!%s' % str(cid)
        return string 
            
    def report2(tup):        
        string = '誠心推薦!!%s, %s' % (tup[0],tup[1])
        return string 
    
    if mongodb.get_ready(uid,'users') ==1 and fmsg1==1:
        get_id(message)
        return 0
    
    if mongodb.get_ready(uid,'users') ==1 and fmsg2==1:
        get_age(message)
        return 0
    
    if mongodb.get_ready(uid,'users') ==1 and fmsg3==1:
        get_gender(message)
        return 0
    
    if message == 'ID':
        choose_id()
        return 0 
    
    if message == '年齡':
        choose_age()
        return 0 
    
    if message == '性別':
        choose_gender()
        return 0 
    
    if message == '清除':
        clear()
        return 0 
    
    if message == '推薦':
        suggest(message,msg3)
        return 0 

    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
    return 0 


if __name__ == '__main__':
    app.run(debug=True)