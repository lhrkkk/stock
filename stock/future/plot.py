#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



from pandas import Series,DataFrame
import pandas as pd
import tushare as ts
from matplotlib import pyplot as plt

import json
# with open('../set/focus.txt','r') as f:
#     # print f.read()
#     all_dict=json.load(f)
#
#     # print all
#     for key in all_dict.keys():
#         all_dict[key]=pd.read_json(all_dict[key])
#     all=pd.Panel(all_dict).transpose("minor","items","major").to_frame()
#     # print all2
#     # print pd.read_json(all['000001'])

data=ts.get_hist_data('sh',ktype='15')
all=data



import matplotlib.pyplot as plt, mpld3

fig=plt.figure()
# plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)


# print all2.ix[['000001','000002']]
# for stock_id in all:
#
#     print all2.ix[stock_id]

# all2=all2['close','ma61','macd']
all['macdbool']=all['dmacdhist']>0
print all


all.ix['000001',['close','ma61','ma131']].plot()





plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

textsize = 9
left, width = 0.1, 0.8
rect1 = [left, 0.7, width, 0.2]
rect2 = [left, 0.3, width, 0.4]
rect3 = [left, 0.1, width, 0.2]


fig = plt.figure(facecolor='white')
axescolor  = '#f6f6f6'  # the axes background color

ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height
ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
ax2t = ax2.twinx()
ax3  = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)

r=all.ix['000001']

### plot the relative strength indicator
prices = r.close
# rsi = relative_strength(prices)
fillcolor = 'darkgoldenrod'

# ax1.plot(r.date, rsi, color=fillcolor)
# ax1.axhline(70, color=fillcolor)
# ax1.axhline(30, color=fillcolor)
# ax1.fill_between(r.date, rsi, 70, where=(rsi>=70), facecolor=fillcolor, edgecolor=fillcolor)
# ax1.fill_between(r.date, rsi, 30, where=(rsi<=30), facecolor=fillcolor, edgecolor=fillcolor)
# ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
# ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
# ax1.set_ylim(0, 100)
# ax1.set_yticks([30,70])
# ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
# ax1.set_title('%s daily'%ticker)

### plot the price and volume data
# dx = r.adj_close - r.close
# low = r.low + dx
# high = r.high + dx
#
# deltas = np.zeros_like(prices)
# deltas[1:] = np.diff(prices)
# up = deltas>0
# ax2.vlines(r.index, r.close, color='black', label='_nolegend_')
# ax2.vlines(r.date[~up], low[~up], high[~up], color='black', label='_nolegend_')
# ma20 = moving_average(prices, 20, type='simple')
# ma200 = moving_average(prices, 200, type='simple')

linema20, = ax2.plot(r.index, r.ma61, color='blue', lw=2, label='MA (20)')
linema200, = ax2.plot(r.index, r.ma131, color='red', lw=2, label='MA (200)')


# last = r[-1]
# s = '%s O:%1.2f H:%1.2f L:%1.2f C:%1.2f, V:%1.1fM Chg:%+1.2f' % (
#     today.strftime('%d-%b-%Y'),
#     last.open, last.high,
#     last.low, last.close,
#     last.volume*1e-6,
#     last.close-last.open )
# t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)
#
# props = font_manager.FontProperties(size=10)
# leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
# leg.get_frame().set_alpha(0.5)
#
#
# volume = (r.close*r.volume)/1e6  # dollar volume in millions
# vmax = volume.max()
# poly = ax2t.fill_between(r.date, volume, 0, label='Volume', facecolor=fillcolor, edgecolor=fillcolor)
# ax2t.set_ylim(0, 5*vmax)
# ax2t.set_yticks([])
#

### compute the MACD indicator
fillcolor = 'darkslategrey'
# nslow = 26
# nfast = 12
# nema = 9
# emaslow, emafast, macd = moving_average_convergence(prices, nslow=nslow, nfast=nfast)
# ema9 = moving_average(macd, nema, type='exponential')
ax3.plot(r.index, r.macd, color='black', lw=2)
# ax3.plot(r.index, ema9, color='blue', lw=1)
# ax3.fill_between(r.date, macd-ema9, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)


# ax3.text(0.025, 0.95, 'MACD (%d, %d, %d)'%(nfast, nslow, nema), va='top',
#          transform=ax3.transAxes, fontsize=textsize)

#ax3.set_yticks([])
# turn off upper axis tick labels, rotate the lower ones, etc

# for ax in ax1, ax2, ax2t, ax3:
#     if ax!=ax3:
#         for label in ax.get_xticklabels():
#             label.set_visible(False)
#     else:
#         for label in ax.get_xticklabels():
#             label.set_rotation(30)
#             label.set_horizontalalignment('right')
#
#     ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')


# class MyLocator(mticker.MaxNLocator):
#     def __init__(self, *args, **kwargs):
#         mticker.MaxNLocator.__init__(self, *args, **kwargs)
#
#     def __call__(self, *args, **kwargs):
#         return mticker.MaxNLocator.__call__(self, *args, **kwargs)

# at most 5 ticks, pruning the upper and lower so they don't overlap
# with other ticks
#ax2.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))
#ax3.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))

# ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
# ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))



# data['close'].plot()
# plt.show()

mpld3.show()

# s=mpld3.fig_to_html(fig)
# open("s.html",'w').write(s)

if __name__ == '__main__':
    pass




from dateutil.parser import parse
# s=parse("2015-07-29 15:00:00 ")
# print s
# new_index=map(parse,data.index)
#
# data.index=new_index
# print data


# print all.index[0]
