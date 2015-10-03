#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# 实时监控推送, 涨停, 涨停开版, 巨量等等


import tushare as ts
import  time
# a=ts.get_today_all()
#
# print a

# df = ts.get_tick_data('600848',date='2014-01-09')
# print df.head(10)


# df = ts.get_realtime_quotes('000581') #Single stock symbol
# print  df[['code','name','price','bid','ask','volume','amount','time']]
import  numpy as np
import  pandas as pd

from stock.state.push import push_to_pushbullet

# symbols from a list
codelist=['000818','000025']
TARGET_NUMBER=-1000

df_new= ts.get_realtime_quotes(codelist)
while 1:
    df_old=df_new
    time.sleep(3)
    df_new= ts.get_realtime_quotes(codelist)
    v_new=df_new[['bid','b1_v','ask','a1_v']].applymap(lambda x:float(x))
    v_old=df_old[['bid','b1_v','ask','a1_v']].applymap(lambda x:float(x))

    v=pd.DataFrame()
    v['name']=df_new['name']
    v['code']=df_new['code']
    # v['b1_v_new']=v_new['b1_v']
    # v['a1_v_new']=v_new['a1_v']
    # v['a1_v_old']=v_old['a1_v']
    # v['b1_v_old']=v_old['b1_v']
    v['买盘变化']=v_new['b1_v']-v_old['b1_v']
    v['卖盘变化']=v_new['a1_v']-v_old['a1_v']

    for i in v['name'].index:
        if abs(v['买盘变化'].ix[i])>TARGET_NUMBER:
            push_object= v[['code','name','买盘变化']].ix[i]
            # print push_object.to_json()
            push_to_pushbullet("买盘变化",push_object)
        if abs(v['卖盘变化'].ix[i])>TARGET_NUMBER:
            push_object=v[['code','name','卖盘变化']].ix[i]
            # print push_object.to_json()
            push_to_pushbullet("卖盘变化",push_object)


            # print df_new
    # print df_new[['name']].join(v_new).join(v_old)

    # v=df_new[['name']].merge(v_new[['bid','b1_v','ask','a1_v']]).merge(v_old[['bid','b1_v','ask','a1_v']])


    # v_delta= v_new[['bid','b1_v','ask','a1_v']].sub(v_old[['bid','b1_v','ask','a1_v']])
    # v_delta.merge(df_new['name'])
    # print v

    # print df_new[['bid','b1_v','ask','a1_v']].sub(df_old[['bid','b1_v','ask','a1_v']])

    # print  df_new[['code','name','price','bid','b1_v','ask','a1_v','volume','amount','time']]

    # print reduce(lambda x,y:x-y, list(df_new[['b1_v']]), list(df_old[['b1_v']]))
    # print list(df_new[['b1_v']]), list(df_old[['b1_v']])
    # print df_new[['b1_v']] ,df_old[['b1_v']]
    # for i in df_new:
    #     print i

    # print np.array(map(int,df_new['b1_v']))-np.array(map(int,df_old['b1_v']))
    # print df_new.add(df_old)

    # print df_new['b1_v']
    # if (int(df_new[['b1_v']])-int(df_old[['b1_v']]))>-1:
    #     print df_new[['b1_v']], df_old[['b1_v']]



#from a Series
# print  ts.get_realtime_quotes(df['code'].tail(10))  #一次获取10个股票的实时分笔数据



#
# #上证指数
# ts.get_realtime_quotes('sh')
# #上证指数 深圳成指 沪深300指数 上证50 中小板 创业板
# ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
# #或者混搭
# ts.get_realtime_quotes(['sh','600848'])
#

if __name__ == '__main__':
    pass


