#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
from stock.common.monkey_patch import as_method_of,as_staticmethod_of


# todo: 定义order和record, portfilio, 针对orderlist自动计算.
# 与其看别人的不如自己实现一个. 读程序不如写程序快.

# 算法的run, 只是把回测也包装进算法里了而已. 计算完毕买卖点(handle_data)之后再自动统计portfilio, 一套做完.

###################################
# 算法: 计算出可供回测的买卖点orderlist.\
#       给出每只股票的评分, 根据评分和T+1规则切换股票. 评分和切换股票的规则构成买卖点. 生成的orderlist提供回测模块画图分析.(原始数据->买卖点)
# 回测: 对买卖点orderlist计算收益率, 给出每笔买卖的收益, 然后累加. 回测的目的是画图分析. 数据都有了. (买卖点数据->分析)
#
#######################
# 买卖单的量怎么算. 一种是只计算买卖点, 回测的时候加入量, 另一种是计算的时候就加入量, 这个时候量应该是个比例.
# 机器学习的算法: 应该给出推定收益率(第二天或3天的), 然后比较收益率选股切换交易给出买卖点.
#
#
# 以上是单只股票操作的模式, 以后再添加组合投资的情形. 包括(原始数据->[算法]->组合买卖list->[回测]->组合list的回测图示)


from pandas import DataFrame

@as_method_of(DataFrame)
def portfilio(self):
    '''
    计算一个dataframe买卖点的portfilio
    :param data: 对已经给出买卖点的dataframe, 按照时间顺序和T+1原则进行计算
    :return:
    '''
    pass


class Orderlist():

    pass

@as_method_of(Orderlist)
def portfilio(self):
    # 计算一个orderlist的portfilio
    pass











if __name__ == '__main__':
    pass


