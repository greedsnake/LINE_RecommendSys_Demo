# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 00:11:54 2018

@author: linzino
"""

from pymongo import MongoClient
import pymongo
import urllib.parse
from datetime import datetime 
import pandas as pd


# db setting
host = 'ds133632.mlab.com'
port = '33632'
username = urllib.parse.quote_plus('username')
password = urllib.parse.quote_plus('userpwd')
# Authentication Database
Authdb='snakedb'

def init_db():
    client = MongoClient('mongodb://%s:%s@%s:%s/%s?authMechanism=SCRAM-SHA-1'
                      % (username, password, host, port, Authdb))
    dbname='snakedb'
    db = client[dbname]
    return db


def insert_one(dic,collection):
    #collection_name = 'users'
    db = init_db()
    coll = db[collection]
    coll.insert_one(dic)


def get_all(collection):
    db = init_db()
    coll = db[collection]
    return list(coll.find())

def find_user(userid,collection):
    '''
    確認這個使用者是不是加入了
    '''
    db = init_db()
    coll = db[collection]
    return len(list(coll.find({"userid":userid})))

def get_all_userid(collection):
    db = init_db()
    coll = db[collection]
    unsers = list(coll.find())
    
    id_list = []
    for user in unsers:
        id_list.append(user['userid'])
    
    return id_list


def get_ready(userid,collection):
    db = init_db()
    coll = db[collection]
    unserinfo = list(coll.find({"userid":userid}))
    return unserinfo[0]['ready']

def update_byid(userid,setdict,collection):
    db = init_db()
    coll = db[collection]
    coll.update({"userid":userid},{"$set":setdict}) 

