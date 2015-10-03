#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


from mongokit import *
from stock.config import MONGO_SERVER,MONGO_PORT,DEBUG
connection = Connection(host=MONGO_SERVER,port=MONGO_PORT)

#
# CONNECTION_STRING = "mongodb://localhost"  # replace it with your settings
# CONNECTION = pymongo.MongoClient(CONNECTION_STRING)
# db=CONNECTION.test.newcollection


# @connection.register
# class SetNames(Document):
#     __database__ = 'stock'
#     __collection__ = 'variables'
#     structure = {
#         "name":basestring,
#         'set_name_list':list,  # 应当是一个字符串的list, 包含set的名字
#         '_type':basestring, # _type filed is for inherit
#     }
#     required_fields = ['name','set_name_list']
#     default_values = {'name' : "set_names","set_name_list": ['focus','all','hold','test']}
#     def update(self,set_names):
#         self.collection.remove({"name":"set_names"})
#         self['set_name_list']=set_names
#         self.save()

# OSL_data15: {'id':000001, 'data':json}
# setlist_name: focus, all, hold,test
# setlist: {set_name:focus, id_list:[]} ,all,hold,test
# stage1/ {"set":"focus_set", "buylist":[], "selllist":[]}
# 函数对于stockid进行stage1计算


@connection.register
class OSL15mk(Document):
    __database__ = 'stock'
    __collection__ = 'OSL_15mk'
    structure = {
        'id':basestring,
        '_type':basestring, # _type filed is for inherit
        'data' : basestring,
        }
    required_fields = ['id', 'data']
    # default_values = {'id' : [],'stock_dict':{},'buy':{}, 'sell':{},'recommend':{},}
    def update(self,id,data):
        self.collection.remove({"id":id})
        self['data']=data
        self.save()


@connection.register
class SetList(Document):
    __database__ = 'stock'
    __collection__ = 'set_list'
    structure = {
        'set_name':basestring,
        '_type':basestring, # _type filed is for inherit
        'id_list' : list,
        }
    # required_fields = ['set_name', 'id_list']
    # default_values = {'id_list' : [],'stock_dict':{},'buy':{}, 'sell':{},'recommend':{},}
    def update(self,set_name,id_list):
        self.collection.remove({"set_name":set_name})
        self['set_name']=set_name
        self['id_list']=id_list
        self.save()


@connection.register
class Stage1(Document):
    __database__ = 'stock'
    __collection__ = 'stage1'
    structure = {
        'set_name':basestring,
        '_type':basestring, # _type filed is for inherit
        'buy_list' : list,
        'sell_list' : list,
        }
    # required_fields = ['set_name', 'buy_list', 'sell_list']
    default_values = {'buy_list' : [],'sell_list':[]}





if __name__ == '__main__':
    pass


