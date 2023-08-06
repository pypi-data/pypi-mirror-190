import os,datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.dates as mdate
mpl.use('Agg')
import matplotlib.pyplot as plt
from . import calc_utils
import dateutil
from . import utils
import warnings
warnings.filterwarnings("ignore")

def get_first_tdates(start_year,end_year):
    time_list = []
    df = utils.trading_dates.copy()
    for year in range(start_year, end_year+1):
        first_day = year * 10000 + 101
        df = df.query("DATE >= @first_day")
        first_tdate = df['DATE'].iloc[0]
        time_list.append(datetime.datetime.strptime(str(first_tdate),'%Y%m%d'))
    return time_list

def plotRline(data_df,x_ticks,ax):
    ax = sns.lineplot(data=data_df, x='date', y='net',label='net',color='#4682B4')#'#5bbfd','0.5'
    ax = sns.lineplot(data= data_df,x ='date',y='after_fee_net',label = 'after_fee_net')
    plt.tick_params(axis='both',which='major',labelsize=12)
    l1 = ax.lines[0]
    x = l1.get_xydata()[:,0]
    y = l1.get_xydata()[:,1]
    
    l2 = ax.lines[1]
    y2 = l2.get_xydata()[:,1]
    ax.fill_between(x,y2,alpha=0.35)
    ax.fill_between(x,y2,y,alpha=0.25,facecolor='#4682B4')

    maxRtn=max(data_df['net'])
    minRtn=min(data_df['after_fee_net'])
    margin=(maxRtn-minRtn)/8
    ax.set_ylim(minRtn-margin,maxRtn+margin)
    ax.set_xlim(data_df['date'].iloc[0],data_df['date'].iloc[-1])
    ax.set_xticks(x_ticks)
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y/%m/%d'))#设置时间标签显示格式

    y_min=np.argmin(y)
    y_max=np.argmax(y)
    maxv = round(y[y_max],4)
    maxdate = data_df.date.iloc[y_max].strftime('%Y/%m/%d')
    minv = round(y[y_min],4)
    mindate = data_df.date.iloc[y_min].strftime('%Y/%m/%d')
    show_min= '['+ mindate+','+ str(minv)+']'
    show_max= '['+ maxdate+','+ str(maxv)+']'
    plt.plot(x[y_min],y[y_min],'kv') 
    plt.plot(x[y_max],y[y_max],'k^')
    plt.annotate(show_min,xy=(x[y_min],y[y_min]),xytext=(data_df['date'].values[y_min],y[y_min]))
    plt.annotate(show_max,xy=(x[y_max],y[y_max]),xytext=(data_df['date'].values[y_max],y[y_max]))

    y_min=np.argmin(y2)
    y_max=np.argmax(y2)
    maxv = round(y2[y_max],4)
    maxdate = data_df.date.iloc[y_max].strftime('%Y/%m/%d')
    minv = round(y2[y_min],4)
    mindate = data_df.date.iloc[y_min].strftime('%Y/%m/%d')
    show_min= '['+ mindate+','+ str(minv)+']'
    show_max= '['+ maxdate+','+ str(maxv)+']'
    plt.plot(x[y_min],y2[y_min],'ko') 
    plt.plot(x[y_max],y2[y_max],'k*')
    plt.annotate(show_min,xy=(x[y_min],y2[y_min]),xytext=(data_df['date'].values[y_min],y2[y_min]))
    plt.annotate(show_max,xy=(x[y_max],y2[y_max]),xytext=(data_df['date'].values[y_max],y2[y_max]))

def plotDDline(data_df,x_ticks):
    data_df.loc[:,'drawdown'] = round((-1 * (data_df['after_fee_net'].cummax()-data_df['after_fee_net'])),5) #single
    ax = sns.lineplot(data=data_df, x='date', y='drawdown', label='ValueWeighted_0.2')
    plt.tick_params(axis='both',which='major',labelsize=12)
    l = ax.lines[0]
    x = l.get_xydata()[:,0]
    y = l.get_xydata()[:,1]
    ax.fill_between(x,y,alpha=0.3)

    maxRtn=max(data_df['drawdown'])
    minRtn=min(data_df['drawdown'])
    margin=(maxRtn-minRtn)/10
    ax.set_ylim(minRtn-margin,maxRtn)
    ax.set_xlim(data_df['date'].iloc[0],data_df['date'].iloc[-1])
    ax.set_xticks(x_ticks)
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y/%m/%d'))#设置时间标签显示格式


def plotRhist(data_df):
    plt.tick_params(axis='both',which='major',labelsize=12)
    sns.histplot(data = data_df,x = 'ret',element="bars", alpha=0.6)

def plottext(ax,indicators,name):    
    ax.plot(facecolor='blue',alpha=0.15)
    ax.set_xlim(-12,10)
    ax.set_ylim(2,23)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    ax.text(-9,20,'Avg Return: %.2f%%'%(indicators['ret']*100),fontsize=16)
    ax.text(-9,16,'Max Drawdown: %.2f%%'%(indicators['max_dd']*100),fontsize=16)
    ax.text(-9,12,'Ret Volatility %.2f%%'%(indicators['ret_std']*100),fontsize=16)
    ax.text(-9,8,'Sharpe: %.2f'%indicators['sharpe'],fontsize=16)
    ax.text(-9,4,'Alpha: %.2f'%indicators['alpha_ret'],fontsize=16)
    ax.text(1,20,'Total Return: %.2f%%'%(indicators['total_ret']*100),fontsize=16)
    ax.text(1,16,'Mdd duration: %s'%indicators['max_dd_date'],fontsize=16)
    ax.text(1,12,'IR: %.2f%%'%(indicators['ir']*100),fontsize=16)
    ax.text(1,8,'Calmar: %.2f'%indicators['calmar'],fontsize=16)
    ax.text(1,4,'beta: %.2f'%indicators['beta'],fontsize=16)
    return ax

def _format(value_list):
    return [str(round(value,4)*100)+'%' for value in value_list]