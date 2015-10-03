#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
from stock.common.monkey_patch import as_method_of,as_staticmethod_of



import tushare as ts
import  numpy as np
from pandas import DataFrame


# df = ts.get_hist_data('000818')
# df = ts.get_tick_data('000818',date='2014-01-09')
# print type(df.index[1])
df=DataFrame()
print df.col


# print df[['close','turnover']]


from pandas import DataFrame
@as_method_of(DataFrame)
def new(self):
    pass



if __name__ == '__main__':
    pass


