#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
## 原始数据为orgin_data提供的setlist和OSLdata(15mk), 根据策略计算买卖点, 并保存buylist和selllist, 用mongodb进行数据的存取.

from stock.common.monkey_patch import as_method_of,as_staticmethod_of
from pandas import Series,DataFrame
import pandas as pd
import  when


from stock.state.db import connection, SetList, OSL15mk

def get_buy_list(set_name,listtype):
    stage1=connection.Stage1().collection.find({'set_name':set_name})
    if listtype=='buy':
        return stage1[0]['buy_list']
    elif listtype=='sell':
        return stage1[0]['sell_list']
    else:
        raise


def buy_sell_point_by_id(id):
    print (id)
    try:
        data= connection.OSL15mk().collection.find({'id':id})[0]['data']
        data=pd.read_json(data)
        # print data
        # macdhist上穿0轴, 61均线斜率大于131均线或者在其上方, 5均线一次导数大于0,二次导数大于等于0, //还需要加入kdj, k>d并且d<20或30
        data['buy_mask']=(data['dmacdhist']>0)&(data['macdhist']>0) & \
                         ((data['macdhist']-data['dmacdhist'])<0 ) & \
                         (( data['dma61']> data['dma131']) |(data['ma61']>data['ma131'])) & \
                         (data['ddma5']>=0)&(data['dma5']>0) & \
                         (data['volume']>=10000)

        # &(data['KDJ_K']>data['KDJ_D']) #& (data['dma61']>-0.1)

        #macdhist下穿0轴, 5日均线斜率小于0,
        data['sell_mask']=(data['dmacdhist']<0)&(data['macdhist']<0) & ((data['macdhist']-data['dmacdhist'])>0 ) & (data['dma5']<=0)
        return  data
    except:
        return False


# todo: 把评分函数抽象出来, 评分->选股->买卖\
# (涉及一个持股周期的问题, 总是最低位置入场, 持股就得时间长, 在上升沿入场, 持股时间短, 选股的时候加入评分排名, 买卖点测试排名), \
# 按时间方向生成买卖点.


# 收入=vt积分,
# 1. 直接看v,[macd~v], 比v有延迟(真实图是macd左移), 是好买点(已经有速度), 卖点延迟(要提前卖,真实的可能已经掉头, 如果掉头就必须卖~真实值低于均线).  macdhist/股价得到比例速度. 可以据此设定阈值和评分.
# 当前买点v有多大, 取决于斜率. 所以[dmacd]是很好的尤其是它积累的量. 然后就是后续力量有多大, dmacd就是力, 如果是正的且大, 那么后续就更看好.
# 因为收入来源于速度, 所以有力没用, 必须有正的速度. 积累的冲量越大, 速度越大. 真实速度也是很好的. (内部有弹性, 能储能.)
# 2. 看v向上的的持续性, ft=mv, f=P/v=dmacd
# 成交量应该可以直接代表价格(有价有市), 代表速度. 净成交量为0点. 代表能量的积蓄和释放. 持续动量代表v的提升.  dmacd=f
# 顶峰没有v的增加, 说明进和出的成交量已经达到平衡了. 同时fs=0, 能量暂时不变. 能量的释放速度=fv, 成交量*v, 如果放量上升或者下跌, 都是越来越快的
#
# 进入的能量(来源于存储的弹性势能和外力)一部分转化成动能, 一部分转化成势能. 还有一部分转化为潜能.
######################################################################
# s/h=价格 日均线直接代表走势. 短均线加速度大于长均线, 或者速度在长均线之上.
# a=dmacd=dv 潜在收益
# v=dma5=dprice=macd  速度, 直接收益. 空头金叉保险
# 归一化, av守恒
#
# todo:
# P=av=单位时间资金净流入, 资金流入柱子. 在力恒定的情况下, 可以等于v. 匀速的时候P外力=-P重力, 加速的时候, P=Fv, 有a=P/mv, 也可以算出外力F,a或者m
# Ep=资金净流入累加
# Ek=速度平方
# 可以根据Ep和Ek的守恒关系计算出m.
# 潜能: Ep-Ek得到潜能, 潜能为0的时候的时候Ep=Ek, 可以计算出m. 潜能不好估算, 可以先算出质量, 再估算潜能. 或者直接用a来代替趋势.
#
#
# 皮球模型: 人的心理习惯->行为的映射 反映到股票上就是皮球模型, 思维模式.   /(另外就是, 和皮球一样, 等你稳定的看到它的时候, 已经在高处速度比较慢了, 所以股市赚钱难)
# ###############################################
# todo:预期收益: 左移macd, 然后用现价和macd趋势, 以及短均线拟合补全
###################

@as_method_of(DataFrame):
def macd_buy_sell(self):

    # macdhist上穿0轴, 61均线斜率大于131均线或者在其上方, 5均线一次导数大于0,二次导数大于等于0, //还需要加入kdj, k>d并且d<20或30
    data['buy_mask']=(data['dmacdhist']>0)&(data['macdhist']>0) & \
                     ((data['macdhist']-data['dmacdhist'])<0 ) & \
                     (data['macd']<0) & (data['macdsignal']<0) & \
                     (( data['dma61']> data['dma131']) |(data['ma61']>data['ma131'])) & \
                     (data['ddma5']>=0)&(data['dma5']>0) & \
                     (data['volume']>=10000)

    data['sell_mask']=(data['dmacdhist']<0)&(data['macdhist']<0) & ((data['macdhist']-data['dmacdhist'])>0 ) & (data['dma5']<=0)




@as_method_of(DataFrame)
def score(self):
    '''
    为dataframe自身计算总得分, 总得分是前面几种算法(能量,功率,av)的综合. 加上当前情况预测的收益率
    :param data: 输入的dataframe
    :return: 返回计算后的data
    '''
    # todo: 完善score, 分开逻辑判断取交集, 或者直接累加
    self['score']=self['av']

    pass






def calc_by_id(id):
    # print id
    try:
        data= connection.OSL15mk().collection.find({'id':id})[0]['data']
        data=pd.read_json(data)
        # print data
        # macdhist上穿0轴, 61均线斜率大于131均线或者在其上方, 5均线一次导数大于0,二次导数大于等于0, //还需要加入kdj, k>d并且d<20或30
        data['buy_mask']=(data['dmacdhist']>0)&(data['macdhist']>0) & \
                         ((data['macdhist']-data['dmacdhist'])<0 ) & \
                         (data['macd']<0) & (data['macdsignal']<0) & \
                         (( data['dma61']> data['dma131']) |(data['ma61']>data['ma131'])) & \
                         (data['ddma5']>=0)&(data['dma5']>0) & \
                         (data['volume']>=10000)
        # &(data['KDJ_K']>data['KDJ_D']) #& (data['dma61']>-0.1)
        #macdhist下穿0轴, 5日均线斜率小于0,
        # todo: 卖出点判断, 买入点加入前面几个周期. 面积小于某某值, 或者计分.
        data['sell_mask']=(data['dmacdhist']<0)&(data['macdhist']<0) & ((data['macdhist']-data['dmacdhist'])>0 ) & (data['dma5']<=0)
        # print data
        # print data['buy_mask']|(data.index>"2015-08-31 11:30:00")
        # start_date = datetime.datetime(yestorrday)

        # todo: 这里处理成时间的形式比较好
        today= str(when.today())+" 09:30:00"
        # print type(data.index[1])
        today_point = data[(data['buy_mask']|data['sell_mask'])&(data.index>today)][['buy_mask','sell_mask']]

        if data.ix[-1]['buy_mask']:
            return ('buy',today_point)
        if data.ix[-1]['sell_mask']:
            return ('sell',today_point)
        return False,False
    except:
        return False,False
#
#
# 计算单个股票
# 按时间遍历, 计算整体算法
# 交易算法的结构
#
# order, orderlist, portfolio,

# todo: 算法只应该生成买卖点
def calc_stage1():
    set_list=connection.SetList().collection.find()
    for stock_set in set_list:
        set_name= stock_set['set_name']
        stage1=connection.Stage1()
        stage1.collection.remove({'set_name':set_name})
        stage1['set_name']=set_name
        stage1['buy_list']=[]
        stage1['sell_list']=[]
        for id in stock_set['id_list']:
            # print set_name, id
            # todo: 这里修改为list
            calcid,today_point=calc_by_id(id)
            if calcid == 'buy':
                stage1['buy_list'].append(id)
                # todo: 设定内容
            elif calcid == 'sell':
                stage1['sell_list'].append(id)
        # print stage1['buy_list']
        # if (set_name == 'focus' or  set_name=='sh' or set_name =='all' )and stage1['buy_list']:
        if stage1['buy_list']:
            push_to_pushbullet(set_name+' buy',stage1['buy_list'])
        elif (set_name == 'hold' or set_name=='sh') and stage1['buy_list']:
            push_to_pushbullet(set_name+' sell',stage1['sell_list'])
        stage1.save()


if __name__=='__main__':
    calc_stage1()


def other():

    import matplotlib.pyplot as plt, mpld3

    fig=plt.figure()
    buy=[]
    sell=[]

    stock_id='000001'
    data= all_dict[stock_id]
    # macdhist上穿0轴, 61均线斜率大于131均线或者在其上方, 5均线一次导数大于0,二次导数大于等于0, //还需要加入kdj, k>d并且d<20或30
    data['buy_mask']=(data['dmacdhist']>0)&(data['macdhist']>0) & \
                     ((data['macdhist']-data['dmacdhist'])<0 ) & \
                     (( data['dma61']> data['dma131']) |(data['ma61']>data['ma131'])) & \
                     (data['ddma5']>=0)&(data['dma5']>0) & \
                     (data['volume']>=10000)

    # &(data['KDJ_K']>data['KDJ_D']) #& (data['dma61']>-0.1)

    #macdhist下穿0轴, 5日均线斜率小于0,
    data['sell_mask']=(data['dmacdhist']<0)&(data['macdhist']<0) & ((data['macdhist']-data['dmacdhist'])>0 ) & (data['dma5']<=0)
    # print data
    print ( data[data['buy_mask']|data['sell_mask']][['buy_mask','sell_mask']])


    exit(0)
    if data.ix[-1]['buy_mask']:
        buy.append(stock_id)
    if data.ix[-1]['sell_mask']:
        sell.append(stock_id)




    for stock_id in all_dict:
        data= all_dict[stock_id]
        # macdhist上穿0轴, 61均线斜率大于131均线或者在其上方, 5均线一次导数大于0,二次导数大于等于0, //还需要加入kdj, k>d并且d<20或30
        data['buy_mask']=(data['dmacdhist']>0)&(data['macdhist']>0) & \
                         ((data['macdhist']-data['dmacdhist'])<0 ) &\
                         (( data['dma61']> data['dma131']) |(data['ma61']>data['ma131'])) & \
                         (data['ddma5']>=0)&(data['dma5']>0) &\
                         (data['volume']>=10000)

                         # &(data['KDJ_K']>data['KDJ_D']) #& (data['dma61']>-0.1)

        #macdhist下穿0轴, 5日均线斜率小于0,
        data['sell_mask']=(data['dmacdhist']<0)&(data['macdhist']<0) & ((data['macdhist']-data['dmacdhist'])>0 ) & (data['dma5']<=0)
        if data.ix[-1]['buy_mask']:
            buy.append(stock_id)
        if data.ix[-1]['sell_mask']:
            sell.append(stock_id)
    # print buy
    # print sell




    exit(0)

    # all2=all2['close','ma61','macd']



    # macdhist上穿0轴, 61均线斜率大于131均线或者在其上方, 5均线一次导数大于0,二次导数大于等于0, //还需要加入kdj, k>d并且d<20或30
    all['buy_mask']=(all['dmacdhist']>0)&(all['macdhist']>0) & ((all['macdhist']-all['dmacdhist'])<0 ) & (( all['dma61']> all['dma131']) |(all['ma61']>all['ma131'])) &(all['ddma5']>=0)&(all['dma5']>0) &(all['KDJ_K']>all['KDJ_D']) #& (all['dma61']>-0.1)

    #macdhist下穿0轴, 5日均线斜率小于0,
    all['sell_mask']=(all['dmacdhist']<0)&(all['macdhist']<0) & ((all['macdhist']-all['dmacdhist'])>0 ) & (all['dma5']<=0)

    # all['coming_mask']=(all['dmacdhist']>0)&(all['macdhist']>0) & ((all['macdhist']-all['dmacdhist'])<0 ) &( all['dma61']> all['dma131']) #& (all['dma61']>-0.1)
    # all['late_mask']=(all['dmacdhist']>0)&(all['macdhist']>0) & ((all['macdhist']-all['dmacdhist'])<0 ) &( all['dma61']> all['dma131']) #& (all['dma61']>-0.1)
    # print all[['KDJ_K','KDJ_D','buy_mask','dmacdhist','dma5','ddma5']]
    print (all[all['buy_mask']][['buy_mask']].irow(-1))

    # all['预警']=all['dmacdhist']>0
    # all['补仓']=all['dmacdhist']>0

    # 移动止损

    # print all


    # all.ix['000001',['close','ma61','ma131']].plot()


