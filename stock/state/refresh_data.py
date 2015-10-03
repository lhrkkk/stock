#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
## 只获取数据到OSL集合, 计算指标, 存入mongodb作为原始数据: 包括选集SetList, 数据OSL15mk


# todo: fix 方法, 只抓取当日, 修正:追加合并行.

from stock.common.monkey_patch import as_method_of,as_staticmethod_of
from pandas import DataFrame




import numpy
import talib
import tushare as ts
from multiprocessing.dummy import Pool as ThreadPool
from time import clock
import os
import datetime
from stock.state.db import connection, OSL15mk, SetList, Stage1
import re
from stock.config import set_name_list, DEBUG
from stock.common.reflection import get_script_location

state_path = get_script_location(__file__)
setpath = os.path.join(state_path, 'set')

start_date = datetime.datetime(2010, 1, 1)
start = clock()


@as_method_of(Dataframe):
def fix(self,new_data):
    # self合并new_data
    pass

def handle_stock(stock_id):
    try:
        f = ts.get_hist_data(stock_id, ktype='15')
        if f is None:
            return

        f.fillna(0)
        f['ma61'] = talib.SMA(numpy.asarray(f['close']), 61)
        f['ma131'] = talib.SMA(numpy.asarray(f['close']), 131)
        f['dma5'] = f['ma5'].diff()
        f['ddma5'] = f['dma5'].diff()
        f['dma61'] = f['ma61'].diff()
        f['dma131'] = f['ma131'].diff()
        f['ddma61'] = f['dma61'].diff()
        f['ddma131'] = f['dma131'].diff()

        f['macd'], f['macdsignal'], f['macdhist'] = talib.MACD(numpy.asarray(f['close']), fastperiod=6, slowperiod=38,
                                                               signalperiod=6)
        f['dmacd'] = f['macd'].diff()
        f['dmacdhist'] = f['macdhist'].diff()
        # stock_dict[stock_id]=f.to_json()

        datadoc = connection.OSL15mk()
        datadoc.collection.remove({'id': stock_id})
        datadoc['data'] = f.to_json()
        datadoc['id'] = stock_id
        datadoc.save()


    except:
        return
        # f=f[['close','ma61','ma131','dma61','ddma61','macd','macdsignal','macdhist','dmacd','dmacdhist']]
        # f.plot(y= ['Close','SMA_20','SMA_50'], title='AAPL Close & Moving Averages')
        # Calculate MACD to be put in a lower panel
        #Plot stacked price and MACD chart
        # plt.subplot(2, 1, 1)
        # plt.gca().axes.get_xaxis().set_visible(False)
        # f.plot(y= ['Close','SMA_20','SMA_50'], title='AAPL Close & Moving Averages')
        # plt.show()
        # plt.subplot(2, 1, 2)
        # f.plot(y= ['macdsignal','macd','macdhist'], title='MACD')
        # plt.show()


def get_set_from_file(set_name_list):
    id_list_of_set = {}
    for set_name in set_name_list:
        file_name = os.path.join(setpath, set_name + '.txt')
        with open(file_name, 'r') as handle:
            text_string = handle.read()

        re_stock_id = re.compile(r'(\d{6})')
        id_list_of_set[set_name] = list(set(re_stock_id.findall(text_string)))
        with open(file_name, 'w') as handle:
            print >> handle, id_list_of_set[set_name]

    # print id_list_of_set
    # todo: 此处强行嵌入了sh

    set_name_list.append('sh')
    id_list_of_set['sh'] = ['sh']
    return id_list_of_set
    # print re_stock_id.findall(text_string)
    # stock_id_list=open('stock_id_list.txt','w')
    # print >>stock_id_list, re_stock_id.findall(text_string)


id_list_of_set = get_set_from_file(set_name_list)

focus_set = {}
all_set = {}
hold_set = {}
test_set = {}

import when, time

print "time is " + str(when.now()).split(":")[1]

from stock.core.algorithm.stage1 import calc_stage1


def get_data(loop=True, period=15, id_list=[], thread_number=8):
    count = 0
    if not loop:
        period = 1
    while True:
        if (int(str(when.now()).split(":")[1]) - 1) % period == 0:
            if count == 0:
                count = 1
                # Make the Pool of workers
                pool = ThreadPool(thread_number)
                # Open the urls in their own threads
                # and return the results
                results = pool.map(lambda x: handle_stock(x), id_list)
                # close the pool and wait for the work to finish
                pool.close()
                pool.join()
                # print all

                # with open("all.txt",'w') as file:
                #     file.write(stock_set.to_json())

                # CONNECTION.test.newcollection.count({"name": "focus"})

                # origin_data=connection.OSL15mk()
                # origin_data['id']='000001'
                # origin_data['data']='helloworld'
                # origin_data.save()
                #
                #
                # focus=connection.stock.Stage1()
                # focus.collection.remove({"name": "focus"})
                # focus['name']='focus'
                # focus['id_list']=focus_id_list
                # focus['stock_dict']=focus_set
                # focus.save()

                # todo: 可以改成用request发送请求的方式. 但是这样更加总是会执行啊好像
                calc_stage1()
                print "ok"
                if loop == False:
                    return
        else:
            count = 0
        time.sleep(1)


#
# 数据库修改api:
# SetNames.update() 等等, 全部都是update

# 每次新建一个数据库项的时候都必须新建一个对象, 否则会在原有对象上面修改, 对象和数据库项是连接在一起的
def init_variables():
    # set_names=connection.SetNames()
    # set_names.update(['all','focus','hold','test'])

    connection.SetList().collection.drop()

    for set_name in set_name_list:
        set_list = connection.SetList()
        set_list.update(set_name, id_list_of_set[set_name])
        #
        # set_list=connection.SetList()
        # set_list.update('hold',hold_id_list)
        # set_list=connection.SetList()
        # set_list.update('test',test_id_list)

        # 滤除all
        # if DEBUG:
        #     set_list=connection.SetList()
        #     set_list.update('all',[])


def get_all_id_list():
    set_list = connection.SetList().collection.find()

    all_id_list = []
    for stock_set in set_list:
        # set_name= stock_set['set_name']
        print stock_set['set_name'], ":", stock_set['id_list']
        all_id_list.extend(stock_set['id_list'])
    all_id_list = set(all_id_list)
    return all_id_list


def get_set_name_list():
    set_list = connection.SetList().collection.find()
    set_name_list = []
    for stock_set in set_list:
        set_name = stock_set['set_name']
        # print stock_set['id_list']
        set_name_list.append(set_name)
    return set_name_list


def get_set_list(set_name):
    set_list = connection.SetList().collection.find({'set_name': set_name})
    return set_list[0]['id_list']


def pull_data():
    init_variables()
    all_id_list = get_all_id_list()
    if DEBUG:
        get_data(loop=False, period=1, id_list=all_id_list)
    else:
        get_data(loop=True, period=15, id_list=all_id_list)


def calc_altorithm():
    pass


if __name__ == '__main__':
    ## 在这里选择是否loop, 以及big_sample还是small_sample, big包含全部股票代码用于实盘,small用于测试
    pull_data()

#     提取数据
#     计算指标
#     给出选股
#





#
#
# def D(n):
#     ans = [None]
#     for i in range(1, len(n)):
#         if n[i - 1] is None:
#             ans.append(None)
#         else:
#             ans.append(n[i] - n[i - 1])
#     return ans
#


# stock_data=f
# low_list = pd.rolling_min(stock_data['low'], 9)
# low_list.fillna(value=pd.expanding_min(stock_data['low']), inplace=True)
# high_list = pd.rolling_max(stock_data['high'], 9)
# high_list.fillna(value=pd.expanding_max(stock_data['high']), inplace=True)
# rsv = (stock_data['close'] - low_list) / (high_list - low_list) * 100
# stock_data['KDJ_K'] = pd.ewma(rsv, com=2)
# stock_data['KDJ_D'] = pd.ewma(stock_data['KDJ_K'], com=2)
# stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
# # 计算KDJ指标金叉、死叉情况
# stock_data['KDJ_金叉死叉'] = ''
# kdj_position = stock_data['KDJ_K'] > stock_data['KDJ_D']
# stock_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
# stock_data.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉'
