import os
import pandas as pd
import datetime
import pymysql
import re
from ..utility import utils
from ..utility.mysqlConnector import mysql_db
from collections import namedtuple
QuotData = namedtuple('QuotData', ['TradingDate', 'Symbol', 'Open', 'High', 'Low', 'Close',
                                   'TotalAmount', 'TotalVolume', 'TotalPosition',
                                   'start_date', 'end_date', 'Exchange', 'FutureType', 'data_type'])


class dataEngine():
    def __init__(self):
        self.data_type = ""
        self.now = utils.globalTimeManager.get_now()
        self.initFlag = True
        self.db = None
        self.mysql_db = mysql_db()
        self.spot_data = None
        self.allFlag = False

    def init(self):
        self.data_type = utils.globalConfig['backtest'].get(
            'dataType', 'DAILY')
        utils.globalCommodityList = [x.lower() for x in list(
            set(utils.globalConfig['backtest']['subscribers']))]
        if "all" in utils.globalCommodityList:
            self.allFlag = True
        self.load_init_data()

    def load_init_data(self):
        # init_year, final_year = utils.globalTimeManager.get_between_year()
        init_date, final_date = utils.globalTimeManager.get_between_date_string()
        start_date = '-'.join([init_date[:4], init_date[4:6], init_date[6:]])
        end_date = '-'.join([final_date[:4], final_date[4:6], final_date[6:]])
        if self.data_type == 'DAILY':
            from clickhouse_driver import Client
            client1 = Client(host='10.66.200.150', port='9000',
                             user='ckdb_u4', password='gtjaqh@2022')
            client2 = Client(host='10.66.200.150', port='9000',
                             user='ckdb_u4', password='gtjaqh@2022')
            settings = {'max_block_size': 100000}
            # load main_contract
            utils.logger.info('Start to load main-contract data from DB!')
            start_date = utils.getNextTradingDate(init_date, -1)
            end_date = utils.getNextTradingDate(final_date)
            exec_sql = f"SELECT formatDateTime(x.date, '%Y%m%d'), upper(x.code), upper(x.contract_real), x.type FROM china_future_day.future_day x WHERE x.date >= '{start_date}' and x.date <= '{end_date}' and x.type in ( 'active', 'next_active') "
            if self.allFlag:
                exec_sql += "ORDER BY x.date, x.contract, x.type"
            else:
                exec_sql += f" and x.code in {utils.globalCommodityList} ORDER BY x.date, x.contract, x.type;"
            result = client1.execute(exec_sql)
            utils.globalContractMap = pd.DataFrame(
                result, columns=['dates', 'commodity', 'contract', 'type'])

            # fetch return data
            utils.logger.info('Start to load return data from DB!')
            return_sql = f"SELECT formatDateTime(x.trading_date,'%Y%m%d'), \
                            x.symbol, toFloat64(x.oc), toFloat64(x.co) \
                            FROM gresearch_factor.china_future_day_oc_co x\
                            where x.trading_date BETWEEN  '{init_date}' and '{final_date}' \
                            order by x.trading_date, x.symbol"
            retunrn_data = client1.execute(return_sql)
            utils.globalReturnData = pd.DataFrame(
                retunrn_data, columns=['TradingDate', 'Symbol', 'OC', 'CO'])
            utils.globalReturnData.fillna(0, inplace=True)

            utils.logger.info('Start to load data from DB!')
            if self.allFlag:
                sql = f"select formatDateTime(x.date, '%Y%m%d') as TradingDate, \
                upper(x.contract) as Symbol, \
                toFloat64(x.open) as Open, \
                toFloat64(x.high) as High, \
                toFloat64(x.low) as Low, \
                toFloat64(x.close) as Close, \
                toFloat64(x.amount) as TotalAmount,\
                toFloat64(x.vol) as TotalVolume, \
                toFloat64(x.oi) as TotalPosition,\
                y.start_date,\
                y.end_date,\
                multiIf(x.exchange='cfe','CFFEX', x.exchange='ine','INE',x.exchange='czc','CZCE',x.exchange='shf','SHFE',x.exchange='dce','DCE','SHFE') as Exchange,\
                x.exchange = 'cfe'?'FF':'CF' as FutureType,\
                'DAILY' as data_type\
                from china_future_day.future_day x , china_baseinfo.contractinfo y \
                where match(x.contract,'^[A-Za-z]+[0-9]+$') and x.date >= '{init_date}' and x.date <= '{final_date}' and x.type='raw' and x.contract = y.contract \
                order by TradingDate, Symbol; "
            else:
                match_list = ['^{}[0-9]+$'.format(x)
                              for x in utils.globalCommodityList]
                sql = f"select formatDateTime(x.date, '%Y%m%d') as TradingDate, \
                upper(x.contract) as Symbol, \
                toFloat64(x.high) as High, \
                toFloat64(x.open) as Open, \
                toFloat64(x.low) as Low, \
                toFloat64(x.close) as Close, \
                toFloat64(x.amount) as TotalAmount,\
                toFloat64(x.vol) as TotalVolume, \
                toFloat64(x.oi) as TotalPosition,\
                y.start_date,\
                y.end_date,\
                multiIf(x.exchange='cfe','CFFEX', x.exchange='ine','INE',x.exchange='czc','CZCE',x.exchange='shf','SHFE',x.exchange='dce','DCE','SHFE') as Exchange,\
                x.exchange = 'cfe'?'FF':'CF' as FutureType,\
                'DAILY' as data_type\
                from china_future_day.future_day x , china_baseinfo.contractinfo y \
                where multiMatchAny(x.contract,{match_list}) and x.date >= '{init_date}' and x.date <= '{final_date}' and x.type='raw' and x.contract = y.contract \
                order by TradingDate, Symbol; "
            self.db = client2.execute_iter(sql, settings=settings)

        spot_sql = f"select date_format(date,'%Y-%m-%d') as date,code as commodity, spot_price_to_future as value from qhadmin.basis_fillin_publish \
                    where date between '{init_date}' and '{final_date}' order by date,code "
        self.spot_data = pd.DataFrame(self.mysql_db.query(
            spot_sql), columns=['date', 'commodity', 'value'])
        utils.logger.warning("Load Data finished!")

    def if_new_day(self, time1, time2):
        if self.data_type == 'DAILY':
            date1 = time1.year*10000 + time1.month*100+time1.day
            date2 = time2.year*10000 + time2.month*100 + time2.day
        return date1 != date2

    def pop_data(self):
        pre_time = utils.globalTimeManager.get_now()
        self.new_day_is_start()
        cur_time = pre_time
        for data_line in self.db:
            cur_quot = QuotData._make(data_line)
            if self.data_type == 'DAILY':
                cur_time = datetime.datetime.strptime(
                    f"{str(cur_quot.TradingDate)} 15:30:00.0", "%Y%m%d %H:%M:%S.%f"
                )
            if self.if_new_day(pre_time, cur_time):  # switch to next trading day
                self.today_is_end()
                self.new_day_is_start()
                pre_time = utils.globalTimeManager.get_now()
            for strategy in utils.globalStrategyDict.values():
                strategy.onDataReceived(cur_quot)
        end_date = utils.globalTimeManager.end_time.strftime("%Y%m%d")
        end_time = utils.globalTimeManager.end_time.strftime("%H:%M:%S")
        utils.logger.info(f"End time is {end_time}")
        if cur_time.strftime("%H:%M:%S") == "15:30:00":
            self.today_is_end()
        if end_date == utils.getNextTradingDate(cur_time.strftime("%Y%m%d")):
            self.new_day_is_start()
        self.all_is_end()

    def new_day_is_start(self):
        this_day = utils.globalTimeManager.get_today()
        spot_data = self.spot_data[self.spot_data['date'] == this_day]
        if self.initFlag:
            self.initFlag = False
        else:
            self.now = utils.globalTimeManager.time_forwards()
        for strategy in utils.globalStrategyDict.values():
            strategy.spot_df = spot_data
            strategy.before_trading()

    def today_is_end(self):
        for strategy in utils.globalStrategyDict.values():
            strategy.after_trading()

    def all_is_end(self):
        for strategy in utils.globalStrategyDict.values():
            # if strategy.stat == 'on':
            strategy.calc_return()
        utils.logger.warning("All is end, bye!")
