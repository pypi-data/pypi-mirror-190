# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
from sklearn import linear_model
from clickhouse_driver import Client
import dateutil
import warnings
warnings.filterwarnings('ignore')
import prettytable as pt

import matplotlib
import matplotlib as mpl  
matplotlib.use('Agg')
import matplotlib.pyplot as plt
mpl.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号  

# auth('15321379946','Tzb123456')
def convert_dt(ss):
    try:
        if type(ss) == str:
            ttt = dateutil.parser.parse(ss)
        else:
            ttt = dateutil.parser.parse(str(ss))
    except Exception as e:
        print(e)
        return
    return ttt.strftime('%Y%m%d')


def get_index():
    # p500 = pd.read_csv(r'/home/Data/baseData/stock_index/p500.csv',index_col = 'dates')
    client = Client(host='10.66.200.150', port='9000',
                    user='ckdb_u4', password='gtjaqh@2022')
    sql = f"SELECT formatDateTime(x.date,'%Y-%m-%d'),\
            toFloat64(x.open), \
            toFloat64(x.close), \
            toFloat64(x.high), \
            toFloat64(x.low), \
            toFloat64(x.vol), \
            toFloat64(x.amount) \
            FROM china_stockindex_day.index_day x \
            WHERE x.code ='000905' ORDER BY x.date"
    result = client.execute(sql)
    client.disconnect()
    p500 = pd.DataFrame(result,columns=['dates','open','close','high','low','volume','money'])
    p500.set_index(keys='dates',inplace=True)
    p500.index = pd.DatetimeIndex(p500.index)
    index_p_dd = {}
    index_p_dd['zz500'] = p500.copy()
    return index_p_dd


def max_dd(df):
    navs = df['nav']
    dates = df['dates']

    peak = 0
    temp_max_dd = 0
    tmp_dd = 0

    dd_ls = []
    fix_duration_ls =[]

    temp_begdate = None
    temp_fix_beg_date = None
    temp_fix_pre_peak = None

    tmp_maxdd_fix_beg_date = None
    tmp_max_pre_peak = None
    maxdd_fix_end_date = None
    maxdd_fix_beg_date = None

    beg_date = None
    end_date = None

    fix_end_date = None
    fix_beg_date = None

    for ii in range(len(navs)):
        n = navs.iloc[ii]
        date = dates.iloc[ii]
        ## Max DrawDown
        if n > peak:
            peak = n
            temp_begdate = date

        if tmp_max_pre_peak is not None and n >= tmp_max_pre_peak:
            maxdd_fix_end_date = date
            maxdd_fix_beg_date = tmp_maxdd_fix_beg_date
            tmp_max_pre_peak = None
            tmp_maxdd_fix_beg_date = None

        drawdown = n - peak
        if drawdown < temp_max_dd:
            temp_max_dd = drawdown
            end_date = date
            beg_date = temp_begdate

            tmp_maxdd_fix_beg_date = date
            tmp_max_pre_peak = peak

        ## Every Drawdown
        if temp_fix_pre_peak is not None and n > temp_fix_pre_peak:
            fix_end_date = date
            fix_beg_date = temp_fix_beg_date
            temp_fix_pre_peak = None
            tmp_fix_duration = (fix_end_date - fix_beg_date).days
            fix_duration_ls.append(tmp_fix_duration)
            if tmp_dd != 0:
                dd_ls.append(tmp_dd)
            tmp_dd = 0

        if drawdown < tmp_dd:
            tmp_dd = drawdown
            temp_fix_beg_date = date
            temp_fix_pre_peak = peak

        if ii == len(navs) - 1 and tmp_dd != 0:
            dd_ls.append(tmp_dd)

    ## drawdown duration
    if peak == 0:
        beg_date = dates.iloc[0]
        end_date = dates.iloc[-1]

    if beg_date is not None:
        drawdown_duration = (end_date - beg_date).days
        beg_date = beg_date.strftime('%Y%m%d')
        end_date = end_date.strftime('%Y%m%d')
    else:
        drawdown_duration = 0

    ### fix_duration
    if tmp_maxdd_fix_beg_date is None:
        fix_duration = (
            (maxdd_fix_end_date - maxdd_fix_beg_date).days
            if maxdd_fix_end_date is not None
            else 0
        )
    elif len(dd_ls) > 1:
        tmp_dd_ls = dd_ls[:-1].copy()
        second_maxdd = min(tmp_dd_ls)
        second_fix_duration = next(
            (
                fix_duration_ls[ddi]
                for ddi in range(len(tmp_dd_ls))
                if tmp_dd_ls[ddi] == second_maxdd
            ),
            0,
        )
        fix_duration = max(second_fix_duration,drawdown_duration)
    else:
        fix_duration = drawdown_duration

    return temp_max_dd,beg_date,end_date,dd_ls,drawdown_duration,fix_duration


def alpha_max_dd(df):
    navs = df['nav']
    dates = df['dates']

    peak = 0
    temp_max_dd = 0
    tmp_dd = 0

    dd_ls = []
    fix_duration_ls = []

    temp_begdate = None
    temp_fix_beg_date = None
    temp_fix_pre_peak = None

    tmp_maxdd_fix_beg_date = None
    tmp_max_pre_peak = None
    maxdd_fix_end_date = None
    maxdd_fix_beg_date = None

    beg_date = None
    end_date = None

    fix_end_date = None
    fix_beg_date = None

    for ii in range(len(navs)):
        n = navs.iloc[ii]
        date = dates.iloc[ii]
        ## Max DrawDown
        if n > peak:
            peak = n
            temp_begdate = date

        if tmp_max_pre_peak is not None and n >= tmp_max_pre_peak:
            maxdd_fix_end_date = date
            maxdd_fix_beg_date = tmp_maxdd_fix_beg_date
            tmp_max_pre_peak = None
            tmp_maxdd_fix_beg_date = None

        drawdown = n - peak
        if drawdown < temp_max_dd:
            temp_max_dd = drawdown
            end_date = date
            beg_date = temp_begdate

            tmp_maxdd_fix_beg_date = date
            tmp_max_pre_peak = peak

        ## Every Drawdown
        if temp_fix_pre_peak is not None and n > temp_fix_pre_peak:
            fix_end_date = date
            fix_beg_date = temp_fix_beg_date
            temp_fix_pre_peak = None
            tmp_fix_duration = (fix_end_date - fix_beg_date).days
            fix_duration_ls.append(tmp_fix_duration)
            if tmp_dd != 0:
                dd_ls.append(tmp_dd)
            tmp_dd = 0

        if drawdown < tmp_dd:
            tmp_dd = drawdown
            temp_fix_beg_date = date
            temp_fix_pre_peak = peak

        if ii == len(navs) - 1 and tmp_dd != 0:
            dd_ls.append(tmp_dd)

    ## drawdown duration
    if peak == 0:
        beg_date = dates.iloc[0]
        end_date = dates.iloc[-1]

    if beg_date is not None:
        drawdown_duration = (end_date - beg_date).days
        beg_date = beg_date.strftime('%Y%m%d')
        end_date = end_date.strftime('%Y%m%d')
    else:
        drawdown_duration = 0

    ### fix_duration
    if tmp_maxdd_fix_beg_date is None:
        fix_duration = (
            (maxdd_fix_end_date - maxdd_fix_beg_date).days
            if maxdd_fix_end_date is not None
            else 0
        )
    elif len(dd_ls) > 1:
        tmp_dd_ls = dd_ls[:-1].copy()
        second_maxdd = min(tmp_dd_ls)
        second_fix_duration = next(
            (
                fix_duration_ls[ddi]
                for ddi in range(len(tmp_dd_ls))
                if tmp_dd_ls[ddi] == second_maxdd
            ),
            0,
        )
        fix_duration = max(second_fix_duration, drawdown_duration)
    else:
        fix_duration = drawdown_duration

    return temp_max_dd,beg_date,end_date,dd_ls,drawdown_duration,fix_duration

def real_ret(df,rollingback_window):
    pick_df = df.copy()
    pick_df = pick_df.sort_values('dates')
    pick_df['dates'] = pd.to_datetime(pick_df['dates'], format="%Y%m%d")
    latest_date = pick_df.iloc[-1]['dates']

    if rollingback_window == 'all':
        pick_nav = pick_df.copy()
    else:
        num_rollingback = int(rollingback_window[:-1])
        freq_rollingback = rollingback_window[-1]

        duration = pd.to_timedelta(num_rollingback, freq_rollingback)
        beg_date = latest_date - duration

        pick_nav = pick_df[pick_df['dates'] >= beg_date]
    if len(pick_nav) == 0:
        return None
    beg_nav = float(pick_nav['nav'].iloc[0])
    return float(pick_nav['nav'].iloc[1]) / beg_nav - 1

def get_alpha_down_std(df):
    navs = df['nav']
    ret_ls = navs.diff(1).astype(float)

    dates_diff = df['dates'].diff()
    dates_interval = dates_diff.apply(lambda x: x.days)
    interval = dates_interval.mean()
    return (
        np.sqrt((np.square(ret_ls[ret_ls < 0])).sum() / (len(ret_ls) - 1 - 1))
        * np.sqrt(365 / interval)
        if len(ret_ls) > 2
        else None
    )


def nav_statistic(df,rollingback_window,index_p,rrf):
    df = df.sort_values('dates')
    df['dates'] = pd.to_datetime(df['dates'], format="%Y%m%d")
    latest_date = df.iloc[-1]['dates']

    if rollingback_window == 'all':
        pick_nav = df.copy()
    else:
        num_rollingback = int(rollingback_window[:-1])
        freq_rollingback = rollingback_window[-1]

        duration = pd.to_timedelta(num_rollingback, freq_rollingback)
        beg_date = latest_date - duration

        pick_nav = df[df['dates'] >= beg_date]
    if len(pick_nav):
        result_dict = {}

        return _extracted_from_nav_statistic_20(pick_nav, result_dict, rrf, index_p)


# TODO Rename this here and in `nav_statistic`
def _extracted_from_nav_statistic_20(pick_nav, result_dict, rrf, index_p):
    ret = get_ret(pick_nav)
    if ret is None:
        return result_dict
    dd, beg_date, end_date, dd_ls, drawdown_duration,fix_duration = max_dd(pick_nav)
    dd = round(float(dd) * -1,4)
    cal_ret_std = get_std(pick_nav)
    if cal_ret_std is None:
        return result_dict

    #### Return Std & Calmar #####
    ret_std = round(cal_ret_std,4)
    if dd == 0:
        calmar = 1000
        result_dict['max_dd_date'] = ''
    else:
        calmar = round(ret / dd,4)
        result_dict['max_dd_date'] = '-'.join([beg_date, end_date])

        ###### Sharpe  #######
    sharpe = 1000 if ret_std == 0 else round((ret-rrf) /ret_std,4)
    ##### Burklin  ######
    cal_dd_std = get_dd_std(dd_ls)
    burklin = (
        1000
        if cal_dd_std is None or cal_dd_std == 0
        else round((ret - rrf) / cal_dd_std, 4)
    )
    ###### Sortino  ########
    cal_down_std = get_down_std(pick_nav)
    if cal_down_std is None or cal_down_std == 0:
        sortino = 1000
    else:
        sortino = round((ret-rrf)/cal_down_std,4)

    ###### Jeason ##########
    beta_ls,jensen_alpha,alpha_std = get_jensen(pick_nav,index_p,rrf)
    beta = None if beta_ls is None else beta_ls[0]
    ###### Infomation Ratio #########
    ab_alpha_ret,alpha_dd,alpha_fix_duration,alpha_down_std = get_absulte_alpha_ret(pick_nav, index_p)
    if ab_alpha_ret is None:
        alpha_dd = None
        alpha_ret = None
    else:
        alpha_dd = round(float(alpha_dd) * -1, 4)
        alpha_ret = get_alpha_ret(pick_nav, index_p)
    if alpha_std is None or alpha_std == 0:
        IR = 1000
    else:
        IR = round(ab_alpha_ret/alpha_std,4)

    if alpha_down_std is None or alpha_down_std == 0:
        IR_sortino = 1000
    else:
        IR_sortino = round(ab_alpha_ret/alpha_down_std,4)

    result_dict['ret'] = ret
    result_dict['max_dd'] = dd
    result_dict['calmar'] = calmar
    result_dict['ret_std'] = ret_std
    result_dict['sharpe'] = sharpe
    result_dict['sortino'] = sortino
    result_dict['drawdown_duration'] = drawdown_duration
    result_dict['burklin'] = burklin
    result_dict['jensen'] = jensen_alpha
    result_dict['ir'] = IR
    result_dict['alpha_ret'] = alpha_ret
    result_dict['ab_annual_alpha_ret'] = ab_alpha_ret
    result_dict['beta'] = beta
    result_dict['alpha_ret_std'] = alpha_std
    result_dict['alpha_dd'] = alpha_dd
    result_dict['fix_duration'] = fix_duration
    result_dict['IR_sortino'] = IR_sortino
    result_dict['alpha_fix_duration'] = alpha_fix_duration

    return result_dict

def get_ret(pick_nav):
    latest_date = pick_nav.iloc[-1]['dates']
    navs = pick_nav['nav']

    nav_beg_date = pick_nav.iloc[0]['dates']
    nav_duration = latest_date - nav_beg_date
    nav_duration_days = nav_duration.days

    if nav_duration_days == 0:
        ret = None
    else:
        ret = round(float(navs.iloc[-1] - navs.iloc[0]) * (365 / nav_duration_days), 4)

    return ret

def get_std(df):
    navs = df['nav']
    ret_ls = (navs.diff(1) / navs.shift(1)).astype(float)
    ret_mean = ret_ls.mean()

    dates_diff = df['dates'].diff()
    dates_interval = dates_diff.apply(lambda x:x.days)
    interval = dates_interval.mean()
    return (
        np.sqrt((np.square(ret_ls - ret_mean)).sum() / (len(ret_ls) - 1 - 1))
        * np.sqrt(365 / interval)
        if len(ret_ls) > 2
        else None
    )

def grade_dd(df, reverse=False):
    ddict = {}
    percentile_ls = list(range(10, 100, 10))
    percentile_ls.append(95)
    for per in percentile_ls:
        percentage = per / 100
        if reverse is False:
            aa = df.quantile(percentage)[0]
            ddict[aa] = round(percentage, 2)
        else:
            aa = df.quantile(1 - percentage)[0]
            ddict[aa] = round(1 - percentage, 2)
    return ddict


def grading(target, benchmark, reverse=False):
    if reverse is False:
        ks = sorted(benchmark.keys())
        grade = None
        for ii in range(len(ks)):
            point = ks[ii]
            if target < point:
                percentage = benchmark[point]
                if percentage == 0.95:
                    grade = 9
                else:
                    grade = percentage * 10 - 1
                break
        if grade is None:
            grade = 10
    else:
        ks = sorted(benchmark.keys(), reverse=True)
        grade = None
        for ii in range(len(ks)):
            point = ks[ii]
            if target > point:
                percentage = benchmark[point]
                # print(ii, point, percentage)
                if percentage == 0.05:
                    grade = 9
                else:
                    grade = 10 - percentage * 10
                break
        if grade is None:
            grade = 10
    return grade

def percentage(target, benchmark, reverse=False):
    if reverse is False:
        ks = sorted(benchmark.keys())
        grade = None
        for ii in range(len(ks)):
            point = ks[ii]
            if target < point:
                percentage = benchmark[point]
                grade = percentage * 10 - 1
                break
        if grade is None:
            grade = 10
    else:
        ks = sorted(benchmark.keys(), reverse=True)
        grade = None
        for ii in range(len(ks)):
            point = ks[ii]
            if target > point:
                percentage = benchmark[point]
                grade = 10 - percentage * 10
                break
        if grade is None:
            grade = 10
    return grade


def get_down_std(df):
    navs = df['nav']
    ret_ls = (navs.diff(1) / navs.shift(1)).astype(float)

    dates_diff = df['dates'].diff()
    dates_interval = dates_diff.apply(lambda x:x.days)
    interval = dates_interval.mean()
    if (len(ret_ls) - 1 - 1) > 0:
        ret_std = np.sqrt((np.square(ret_ls[ret_ls<0])).sum() / (len(ret_ls) - 1 - 1)) * np.sqrt(365 /interval)
    else:
        ret_std = None

    return ret_std

def get_dd_std(dd_ls):
    sum = 0
    for dd in dd_ls:
        sum += float(dd)**2
    dd_std = sum**0.5
    return dd_std

def get_jensen(df,index_p,rrf):
    if index_p is None:
        return None,None,None

    tmp_df = df.copy()
    # dates = pd.to_datetime(tmp_df['dates'])
    tmp_df = tmp_df.set_index('dates')
    tmp_df = tmp_df

    index_p = index_p.drop_duplicates()
    tmp_df = tmp_df.drop_duplicates()

    try:
        # tmp_total = pd.concat([tmp_df,index_p],axis = 1)
        tmp_total = pd.merge(tmp_df, index_p, how='left', left_index=True,right_index=True)
    except:
        print('error')
    tmp_total = tmp_total.dropna(how='any')

    tmp_total['nav'] = tmp_total['nav'].astype(float)
    tmp_total['nav_ret'] = tmp_total['nav'].pct_change()
    tmp_total['index_ret'] = tmp_total['close'].pct_change()
    tmp_total = tmp_total.dropna(how='any')

    if len(tmp_total) == 0:
        return None, None, None

    model = linear_model.LinearRegression()
    x = np.array(tmp_total['index_ret']-rrf).reshape(-1,1)
    y = np.array(tmp_total['nav_ret']-rrf).reshape(-1,1)
    model.fit(x,y)

    coef = model.coef_[0]
    intercept = model.intercept_[0]

    tmp_error = tmp_total['nav_ret'] - tmp_total['index_ret']

    aa = tmp_error.reset_index()
    aa.columns = ['dates','nav']
    ret_mean = tmp_error.mean()
    dates_diff = aa['dates'].diff()
    dates_interval = dates_diff.apply(lambda x: x.days)
    interval = dates_interval.mean()
    if (len(tmp_error) - 1 - 1) > 0:
        ret_std = np.sqrt((np.square(tmp_error - ret_mean)).sum() / (len(tmp_error) - 1 - 1)) * np.sqrt(365 / interval)
    else:
        ret_std = None

    return coef,intercept,ret_std

def get_alpha_ret(df,index_p):
    if index_p is None:
        return None

    tmp_df = df.copy()
    tmp_df = tmp_df.set_index('dates')

    # tmp_total = pd.concat([tmp_df, index_p], axis=1)
    tmp_total = pd.merge(tmp_df, index_p,how='left',left_index=True, right_index=True)    
    tmp_total = tmp_total.dropna(how='any')

    tmp_total['nav'] = tmp_total['nav'].astype(float)
    tmp_total['nav_ret'] = tmp_total['nav'].pct_change()
    tmp_total['index_ret'] = tmp_total['close'].pct_change()
    tmp_total = tmp_total.dropna(how='any')

    if len(tmp_total) == 0:
        return None

    tmp_error = tmp_total['nav_ret'] - tmp_total['index_ret']

    alpha_return = tmp_error.sum()

    return alpha_return

def get_absulte_alpha_ret(df,index_p):
    tmp_df = df.copy()

    latest_date = tmp_df.iloc[-1]['dates']
    nav_beg_date = tmp_df.iloc[0]['dates']
    nav_duration = latest_date - nav_beg_date
    nav_duration_days = nav_duration.days
    tmp_df = tmp_df.set_index('dates')
    # tmp_total = pd.concat([tmp_df, index_p], axis=1)
    tmp_total = pd.merge(tmp_df, index_p,how='left',left_index=True, right_index=True)
    tmp_total = tmp_total.dropna(how='any')

    if len(tmp_total) == 0:
        return None,None,None,None

    tmp_total['nav'] = tmp_total['nav'].astype(float)
    tmp_total['close'] = tmp_total['close'].astype(float)

    nav_ret = tmp_total.iloc[-1]['nav'] / tmp_total.iloc[0]['nav'] - 1
    index_ret = tmp_total.iloc[-1]['close'] / tmp_total.iloc[0]['close'] - 1


    if nav_duration_days == 0:
        ab_alpha_ret = None
    else:
        nav_annual_ret = round(float(nav_ret + 1) ** (365 / nav_duration_days) - 1, 4)
        index_annual_ret = round(float(index_ret + 1) ** (365 / nav_duration_days) - 1, 4)
        ab_alpha_ret = nav_annual_ret - index_annual_ret

    tmp_err_nav = tmp_total['nav'] / tmp_total.iloc[0]['nav'] - 1
    tmp_err_index_ret = tmp_total['close'] / tmp_total.iloc[0]['close'] - 1
    tmp_err = tmp_err_nav - tmp_err_index_ret
    tmp_err = tmp_err.reset_index()
    tmp_err.columns = ['dates','nav']
    alpha_temp_dd, alpha_beg_date, alpha_end_date, alpha_dd_ls, alpha_drawdown_duration,alpha_fix_duration = alpha_max_dd(tmp_err)
    alpha_down_std = get_alpha_down_std(tmp_err)

    return ab_alpha_ret,alpha_temp_dd,alpha_fix_duration,alpha_down_std


if __name__ == "__main__":
    index_benchmark = get_index()
    df_net = pd.read_csv(r'/home/Data/factors/hjt/Basis_Factor/output/Basis_Factor/return/return.csv',dtype = {'date' : str})
    df_net.rename(columns = {"date": "dates","net":"nav"},inplace = True)
    result = {}
    for portfolio,df_each in df_net.groupby('portfolio'):
        df_each['dates'] = df_each['dates'].apply(lambda x:datetime.datetime.strptime(x,'%Y%m%d'))    
        result_dict = nav_statistic(df_each[['dates','nav']],'all',index_benchmark['zz500'], 0)
        result[portfolio] = result_dict
    # for line in result_list:    
        # print(line)

    tb = pt.PrettyTable()
    tb.field_names = ["portfolio", "return", "ret_std","calmar","sharpe","max_dd","max_dd_date", "fix_duration"]
    for portfolio, result_dict in result.items():
        tb.add_row([portfolio, result_dict['ret'],result_dict['ret_std'], result_dict['calmar'], result_dict['sharpe'],result_dict['max_dd'],result_dict['max_dd_date'],result_dict['fix_duration']])
    print(tb)

