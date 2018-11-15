# -*- coding: utf-8 -*-

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
import pandas as pd
import MTF

# ---------------------------------------------------------------------
# Load data 
path = ['data/', 'result/']
file = ['client', 'all_data']
res_file = ['group_top_n_brand', 'group_top_n_category', 'group_top_n_pair']
res_file2 = ['top_n_brand','top_n_category','top_n_cb']
id_file = ['recommand_brand','recommand_category','recommand_brand_category']
df_group_brand_res = pd.read_csv(f'{path[1]}{res_file[0]}.csv', encoding='utf8')
df_group_cat_res = pd.read_csv(f'{path[1]}{res_file[1]}.csv', encoding='utf8')
df_group_cb_res = pd.read_csv(f'{path[1]}{res_file[2]}.csv', encoding='utf8')
df_id_brand_res = pd.read_csv(f'{path[1]}{id_file[0]}.csv', encoding='utf8',index_col='Unnamed: 0')
df_id_cate_res = pd.read_csv(f'{path[1]}{id_file[1]}.csv', encoding='utf8',index_col='Unnamed: 0')
df_id_cb_res = pd.read_csv(f'{path[1]}{id_file[2]}.csv', encoding='utf8',index_col='Unnamed: 0')
id_list = list(df_id_brand_res.index)
# ---------------------------------------------------------------------

app = Flask(__name__)

line_bot_api = LineBotApi('tALJGyw5Gzes13Eo59pE+eRR5fV11Dw6SYCshuxGkwjaMr+PEI+EeKY9YzoUyERZIccZqD4zTt4LKtYkVQINT1eOEgZaPtAReN+Oc2V8hsmbNgNsw+SnQDuqDLo8EzR1+7ID/7KkCNCbmMURnvxhQQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ee211365f9ec399943c478989fe2eed5')

msg1 = msg2 = msg3 = ""
fid1 = fid2 = fid3 = 0
fgroup1 = fgroup2 = fgroup3 = 0
cmd='您還沒輸入任何指令'
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
      remessage = TextSendMessage(text='請輸入客戶編號')
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
      
    def get_id1(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg1,fid1
      fid1 = 0
      msg1 = str(message)
      if msg1 in id_list:
          remessage = TextSendMessage(text='推薦客戶編號%s的品牌：\n%s, %s, %s' % \
                                      (msg1, df_id_brand_res.loc[msg1][0], df_id_brand_res.loc[msg1][1], \
                                       df_id_brand_res.loc[msg1][2]) )
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
      else:
          remessage = TextSendMessage(text='無此客戶')
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
      
    def get_id2(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg1,fid2
      fid2 = 0
      msg1 = str(message)
      if msg1 in id_list:
          remessage = TextSendMessage(text='推薦客戶編號%s的類別：\n%s, %s, %s' % \
                                      (msg1, df_id_cate_res.loc[msg1][0], df_id_cate_res.loc[msg1][1], \
                                       df_id_cate_res.loc[msg1][2]) )
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
      else:
          remessage = TextSendMessage(text='無此客戶')
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
          
    def get_id3(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg1,fid3
      fid3 = 0
      msg1 = str(message)
      if msg1 in id_list:
          remessage = TextSendMessage(text='推薦客戶編號%s的商品：\n%s-%s\n%s-%s\n%s-%s' % \
                                      (msg1, eval(df_id_cb_res.loc[msg1][0])[1], eval(df_id_cb_res.loc[msg1][0])[0], \
                                       eval(df_id_cb_res.loc[msg1][1])[1], eval(df_id_cb_res.loc[msg1][1])[0], \
                                       eval(df_id_cb_res.loc[msg1][2])[1], eval(df_id_cb_res.loc[msg1][2])[0]) )
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
      else:
          remessage = TextSendMessage(text='無此客戶')
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
      
    def choose_group():
      # 設定使用者下一句話要群廣播
      mongodb.update_byid(uid,{'ready':1},'users')
      remessage = TextSendMessage(text="請輸入客戶年齡及性別(age,gender)\n女性請填'0',男性請填'1'")
      line_bot_api.reply_message(
                      event.reply_token,
                      remessage)
           
    def get_group1(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg2,fgroup1
      bins = [0, 19, 21, 23, 33, 41, 101]
      fgroup1 = 0
      transex(message)
      if msg2=='error':
          remessage = TextSendMessage(text='資料輸入錯誤')
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
      else:
          try:
              group = MTF.insert_trans(msg2,bins)
              if msg2[1]==0:
                  sug = MTF.tar_recommand(df_group_brand_res, 'group', group, ['brand'])
              elif msg2[1]==1:
                  sug = pd.read_csv(path[1]+res_file2[0]+'.csv', encoding='utf8', header=None).head(3)
                  sug.columns= ['brand','score']
              remessage = TextSendMessage(text='推薦%s歲%s客戶的品牌：\n%s, %s, %s' % \
                                          (msg2[0], sex,sug.brand[sug.index[0]], \
                                           sug.brand[sug.index[1]], sug.brand[sug.index[2]] ))
              line_bot_api.reply_message(
                              event.reply_token,
                              remessage)
          except:
              errorinput()          
          
    def get_group2(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg2,fgroup2
      bins = [0, 19, 21, 23, 33, 41, 101]
      fgroup2 = 0
      transex(message)
      if msg2=='error':
          remessage = TextSendMessage(text='資料輸入錯誤')
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
      else:
          try:
              group = MTF.insert_trans(msg2,bins)
              if msg2[1]==0:
                  sug = MTF.tar_recommand(df_group_cat_res, 'group', group, ['category'])
              elif msg2[1]==1:
                  sug = pd.read_csv(path[1]+res_file2[1]+'.csv', encoding='utf8').head(3)
              remessage = TextSendMessage(text='推薦%s歲%s客戶的類別：\n%s、%s、%s' % \
                                          (msg2[0], sex, sug.category[sug.index[0]], \
                                           sug.category[sug.index[1]], sug.category[sug.index[2]] ))
              line_bot_api.reply_message(
                              event.reply_token,
                              remessage)
          except:
              errorinput()          
      
    def get_group3(message):    
      mongodb.update_byid(uid,{'ready':0},'users')
      global msg2,fgroup3
      bins = [0, 19, 21, 23, 33, 41, 101]
      fgroup3 = 0
      transex(message)
      if msg2=='error':
          remessage = TextSendMessage(text='資料輸入錯誤')
          line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
      else:
          try:
              group = MTF.insert_trans(msg2,bins)
              if msg2[1]==0:
                  sug = MTF.tar_recommand(df_group_cb_res, 'group', group, ['category', 'brand'])
              elif msg2[1]==1:
                  sug = pd.read_csv(path[1]+res_file2[2]+'.csv', encoding='utf8').head(3)
              remessage = TextSendMessage(text='推薦%s歲%s客戶的商品：\n%s-%s\n%s-%s\n%s-%s' % \
                                          (msg2[0], sex, sug.brand[sug.index[0]], sug.category[sug.index[0]], \
                                           sug.brand[sug.index[1]], sug.category[sug.index[1]], \
                                           sug.brand[sug.index[2]], sug.category[sug.index[2]] ))
              line_bot_api.reply_message(
                              event.reply_token,
                              remessage)
          except:
              errorinput() 
      
    def transex(message):
      global msg2,sex
      msg2 = message
      msg2 = msg2.replace('，',',')
      msg2 = msg2.split(',')         
      if msg2[1]=='0':
          sex='女性'
      elif msg2[1]=='1':
          sex='男性'
      else:
          sex=''
      try:
          msg2[0]=int(msg2[0])
          msg2[1]=int(msg2[1])
          msg2 = tuple(msg2)
      except ValueError:
          msg2 = 'error'
      return 0
    
    def errorinput():
        if msg2[0]<0 or msg2[0]>100:
            remessage = TextSendMessage(text='無此年齡區間')
            line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
        elif msg2[1]!=0 or msg2[1]!=1:
            remessage = TextSendMessage(text='無此性別')
            line_bot_api.reply_message(
                          event.reply_token,
                          remessage)
        else:
            remessage = TextSendMessage(text='資料輸入錯誤')
            line_bot_api.reply_message(
                          event.reply_token,
                          remessage)

    def report1(cid):        
        string = '誠心推薦!!%s' % str(cid)
        return string 
            
    def report2(tup):        
        string = '誠心推薦!!%s, %s' % (tup[0],tup[1])
        return string 
    
    if message == 'ID-品牌':
        global fid1
        fid1 = 1
        choose_id()
        return 0     
    
    if message == 'ID-類別':
        global fid2
        fid2 = 1
        choose_id()
        return 0 
    
    if message == 'ID-品牌類別':
        global fid3
        fid3 = 1
        choose_id()
        return 0 
    
    if message == '族群-品牌':
        global fgroup1
        fgroup1 = 1
        choose_group()
        return 0     
    
    if message == '族群-類別':
        global fgroup2
        fgroup2 = 1
        choose_group()
        return 0 
    
    if message == '族群-品牌類別':
        global fgroup3
        fgroup3 = 1
        choose_group()
        return 0   
    
    if mongodb.get_ready(uid,'users') ==1 and fid1==1:
        get_id1(message)
        return 0
    
    if mongodb.get_ready(uid,'users') ==1 and fid2==1:
        get_id2(message)
        return 0
    
    if mongodb.get_ready(uid,'users') ==1 and fid3==1:
        get_id3(message)
        return 0
    
    if mongodb.get_ready(uid,'users') ==1 and fgroup1==1:
        get_group1(message)
        return 0
    
    if mongodb.get_ready(uid,'users') ==1 and fgroup2==1:
        get_group2(message)
        return 0
    
    if mongodb.get_ready(uid,'users') ==1 and fgroup3==1:
        get_group3(message)
        return 0
    

    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
    return 0 


if __name__ == '__main__':
    app.run(debug=True)