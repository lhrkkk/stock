#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
from stock.common.monkey_patch import as_method_of,as_staticmethod_of


#todo: 只是普通策略, 则只需要简单计算portfilio, 对于学习策略, 要添加分段功能.
# portfilio画图


# from portfilio import DataFrame
# import pandas as pd
from pandas import DataFrame
# 对象不存在名字空间, 都是导入到这里的

import portfilio
import analysis


@as_method_of(DataFrame)
def plot_portfilio(self):
    pass





s=DataFrame()

s.plot_portfilio()






if __name__ == '__main__':
    pass


