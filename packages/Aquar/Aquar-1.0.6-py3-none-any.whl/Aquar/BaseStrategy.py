
from abc import ABC, abstractmethod
from .utility import utils
from .utility import calc_utils
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from .utility.plotReturn import *
import warnings
warnings.filterwarnings("ignore")
os.environ['NUMEXPR_MAX_THREADS'] = '32'
os.environ['NUMEXPR_NUM_THREADS'] = '8'


class BaseStrategy(ABC):
    def __init__(self, author, name, st_name='strategy'):
        self.author = author
        self.name = name
        self.factor_dir = os.path.join('output', self.name, 'factor')
        self.position_dir = os.path.join("output", self.name, 'position')
        self.newFlag = utils.globalConfig[st_name].get('newFlag', 'True')
        # utils.globalConfig['trade'].get('commission_CF', 3)
        self.commission_CF = 3
        # utils.globalConfig['trade'].get('commission_FF', 0.23)
        self.commission_FF = 0.23
        # self.slippage = utils.globalConfig['trade'].get('slippage', 1)
        if not os.path.exists(self.factor_dir):
            os.makedirs(self.factor_dir)
        elif self.newFlag == "True":
            os.system(f"rm -rf {self.factor_dir}/*")

        if not os.path.exists(self.position_dir):
            os.makedirs(self.position_dir)
        elif self.newFlag == "True":
            os.system(f"rm -rf {self.position_dir}/*")
        self.contract_dict = {0: 'active', 1: 'next_active'}
        self.stat = utils.globalConfig[st_name].get('stat', 'on')
        self.stat_type = utils.globalConfig[st_name].get('stat_type', 'CS')
        self.df_day = pd.DataFrame(columns=['date', 'portfolio', 'day_pnl'])
        self.df_night = pd.DataFrame(
            columns=['date', 'portfolio', 'night_pnl'])
        self.return_df = pd.DataFrame()
        self.return_dir = os.path.join('output', self.name, 'return')
        self.spot_df = pd.DataFrame(columns=['commodity', 'value'])
        self.last_date = float('-inf')
        if self.newFlag == 'True':
            if not os.path.exists(self.return_dir):
                os.makedirs(self.return_dir)
            else:
                os.system(f"rm -rf {self.return_dir}/* ")
        else:
            if not os.path.exists(self.return_dir):
                os.makedirs(self.return_dir)
            if os.path.exists(os.path.join(self.return_dir, '.pickler_day')) and os.path.join(self.return_dir, '.pickler_night'):
                self.df_day = pd.read_pickle(
                    os.path.join(self.return_dir, '.pickler_day'))
                self.df_night = pd.read_pickle(
                    os.path.join(self.return_dir, '.pickler_night'))

    def regist(self):
        utils.globalStrategyDict[self.name] = self

    @abstractmethod
    def onDataReceived(self, MarketData):
        pass

    def onTimerTriggered(self):
        pass

    def registTimer(self):
        pass

    def loadParams(self):
        pass

    def before_trading(self):
        self.spot_df.loc[:, 'commodity'] = self.spot_df.loc[:,
                                                            'commodity'].str.upper()

    def after_trading(self):
        self.calc_profit()

    def get_spot_price(self, CommodityList):
        if 'ALL' in CommodityList:
            return self.spot_df[['commodity', 'value']].set_index('commodity')['value'].to_dict()
        CommodityList = [x.upper() for x in CommodityList]
        result = self.spot_df.query('commodity in @CommodityList')
        return result.set_index('commodity')['value'].to_dict()

    def get_contract(self,  TDate, CommodityList, type=0):
        # type = 0：main_contract; 1:sub_main_contract;
        # type = 3：active_contract; 1:sub_active_contract;
        # 2022-12-01 only provide main_contract info
        true_date = utils.getNextTradingDate(TDate, -1)
        type_name = self.contract_dict.get(type, 'active')
        if 'ALL' in CommodityList:
            s = utils.globalContractMap.query(
                f'dates=="{true_date}" and type=="{type_name}" ')
        else:
            s = utils.globalContractMap.query(
                f'dates=="{true_date}" and commodity in @CommodityList and type=="{type_name}" ')

        sf = s[['commodity', 'contract']].copy()
        sf.dropna(axis=0, how='any', inplace=True)

        return sf.set_index('commodity')['contract'].to_dict()

    def get_now(self):
        return utils.globalTimeManager.get_now()

    def get_Config(self):
        return utils.globalConfig

    def get_this_day(self):
        now_time = self.get_now()
        return str(now_time.year*10000+now_time.month*100+now_time.day)

    def storeFactorValue(self, val_df):
        utils.assert_msg(len(val_df.columns & {'contract', 'value'}) == 2,
                         ("输入的`FactorValue Dataframe`格式不正确，至少需要包含这些列："
                          "'contract', 'value'"))
        file_name = '_'.join(
            [self.author, self.name, self.get_this_day()+'.csv'])
        file_path = os.path.join(self.factor_dir, file_name)
        val_df.to_csv(file_path, index=False)

    def storePosition(self, pos_df):
        utils.assert_msg(len(pos_df.columns & {'portfolio', 'contract', 'o', 'c'}) == 4,
                         ("输入的`Positon Dataframe`格式不正确，至少需要包含这些列："
                          "'portfolio','contract', 'o', 'c'"))
        file_name = '_'.join(
            [self.author, self.name, self.get_this_day()+'.csv'])
        file_path = os.path.join(self.position_dir, file_name)
        cols = ['portfolio', 'contract', 'o', 'c', 'day_pnl',
                'day_turnover', 'night_pnl', 'night_turnover']
        df = pos_df.reindex(columns=cols, fill_value=0)
        df.to_csv(file_path, index=False, float_format='%.6f')

    def calc_profit(self, is_latest_day=False):
        this_date = self.get_this_day()
        pre_date = utils.getNextTradingDate(this_date, -1)
        file_name = '_'.join((self.author, self.name, pre_date + '.csv'))
        file_path = os.path.join(self.position_dir, file_name)
        if not os.path.exists(file_path):
            return
        pre_pos_df = pd.read_csv(file_path)
        pre_return_df = utils.globalReturnData[utils.globalReturnData['TradingDate'] == pre_date]
        if not is_latest_day:
            return_df = utils.globalReturnData[utils.globalReturnData['TradingDate'] == this_date]
        else:
            return_df = pre_return_df.copy()
            return_df['OC'] = 0
            return_df['CO'] = 0
        new_pos_df = pd.DataFrame()
        row_day_list, row_night_list = [], []
        this_file_name = '_'.join((self.author, self.name, this_date + '.csv'))
        this_file_path = os.path.join(self.position_dir, this_file_name)
        this_pos_df = (
            pd.read_csv(this_file_path)
            if os.path.exists(this_file_path)
            else pd.DataFrame(
                columns=['portfolio', 'contract',
                         'o', 'c', 'day_pnl', 'night_pnl']
            )
        )
        for pf, pf_df in pre_pos_df.groupby('portfolio'):
            pre_df = pd.merge(pf_df, pre_return_df, how='left', left_on='contract', right_on='Symbol')[
                ['portfolio', 'contract', 'o', 'c', 'OC', 'CO']]
            pre_df['day_pnl'] = pre_df.eval('o*OC')
            df = pd.merge(pf_df, return_df, how='left', left_on='contract', right_on='Symbol')[[
                'portfolio', 'contract', 'o', 'c',
                'OC', 'CO']]
            pre_df['night_pnl'] = df.eval('c*CO')
            pre_df.fillna(0, inplace=True)
            to_df = pd.merge(left=pf_df, right=(this_pos_df[this_pos_df['portfolio'] == pf]), on=['portfolio', 'contract'], how='outer', suffixes=('_pre',
                                                                                                                                                   '_today'))
            to_df.fillna(0, inplace=True)
            to_df['night_turnover'] = (to_df['c_pre'] - to_df['o_today']).abs()
            to_df['day_turnover'] = (to_df['o_pre'] - to_df['c_pre']).abs()
            pre_df['night_turnover'] = to_df['night_turnover']
            pre_df['day_turnover'] = to_df['day_turnover']
            pre_df_FF = pre_df[pre_df['contract'].str.startswith(('IC', 'IH', 'IF',
                                                                  'IM'))]
            pre_df_FF['day_fee'] = pre_df_FF.eval(
                'day_turnover * 15 * @self.commission_FF / 10000')
            pre_df_FF['night_fee'] = pre_df_FF.eval(
                'night_turnover * @self.commission_FF / 10000')
            pre_df_CF = pre_df[~pre_df['contract'].str.startswith(('IC', 'IH', 'IF',
                                                                   'IM'))]
            pre_df_CF['day_fee'] = pre_df_CF.eval(
                'day_turnover * @self.commission_CF / 10000')
            pre_df_CF['night_fee'] = pre_df_CF.eval(
                'night_turnover * @self.commission_CF / 10000')
            pre_df = pd.concat([pre_df_FF, pre_df_CF], axis=0)
            new_pos_df = pd.concat([new_pos_df, pre_df], axis=0)
            row_dict = {'date': pre_date,  'portfolio': pf,  'day_pnl': pre_df['day_pnl'].sum(
            ),  'day_turnover': to_df['day_turnover'].sum(),  'day_fee': pre_df['day_fee'].sum()}
            row_day_list.append(row_dict)
            row_dict = {'date': this_date,  'portfolio': pf,  'night_pnl': pre_df['night_pnl'].sum(
            ),  'night_turnover': to_df['night_turnover'].sum(),  'night_fee': pre_df['night_fee'].sum()}
            row_night_list.append(row_dict)
        self.df_day = self.df_day[~self.df_day['date'].isin([pre_date])]
        self.df_night = self.df_night[~self.df_night['date'].isin([this_date])]
        self.df_day = pd.concat(
            [self.df_day, pd.DataFrame(row_day_list)], axis=0)
        self.df_night = pd.concat(
            [self.df_night, pd.DataFrame(row_night_list)], axis=0)
        new_pos_df[['portfolio', 'contract', 'o', 'c', 'day_pnl', 'day_turnover',
                    'night_pnl', 'night_turnover']].to_csv(file_path, index=False, float_format='%.6f')

    def calc_nav_indicators(self):
        index_benchmark = calc_utils.get_index()
        df_net = pd.read_csv(os.path.join(
            self.return_dir, 'return.csv'), dtype={'date': str})
        df_net.rename(columns={"date": "dates", "net": "nav"}, inplace=True)
        result = {}
        for portfolio, df_each in df_net.groupby('portfolio'):
            df_each['dates'] = df_each['dates'].apply(
                lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
            result_dict = calc_utils.nav_statistic(
                df_each[['dates', 'nav']], 'all', index_benchmark['zz500'], 0)
            result[self.name+'_'+portfolio] = result_dict
        return result

    def calc_return(self):
        if self.df_day.empty:
            print('empty')
            return
        self.calc_profit(is_latest_day=True)
        this_date = self.get_this_day()
        pre_date = utils.getNextTradingDate(this_date, -1)
        self.return_df = pd.merge((self.df_day), (self.df_night), on=[
                                  'date', 'portfolio'], how='left')
        self.df_day[['date', 'portfolio', 'day_pnl', 'day_turnover']].to_pickle(
            os.path.join(self.return_dir, '.pickler_day'))
        self.df_night[['date', 'portfolio', 'night_pnl', 'night_turnover']].to_pickle(
            os.path.join(self.return_dir, '.pickler_night'))
        self.return_df.fillna(0, inplace=True)
        self.return_df['total_pnl'] = self.return_df.eval(
            'day_pnl + night_pnl ')
        self.return_df['after_fee_pnl'] = self.return_df.eval(
            'day_pnl + night_pnl - day_fee - night_fee')
        self.return_df.sort_values(by=['portfolio', 'date'], inplace=True)
        self.return_df['net'] = self.return_df.groupby(
            'portfolio')['total_pnl'].cumsum() + 1
        self.return_df['after_fee_net'] = self.return_df.groupby(
            'portfolio')['after_fee_pnl'].cumsum() + 1
        df_ret = pd.DataFrame()
        for pf, df_pf in self.return_df.groupby('portfolio'):
            df_pf['r1'] = np.log(df_pf['after_fee_net'].shift(1).fillna(1))
            df_pf['r2'] = np.log(df_pf['after_fee_net'][:])
            df_pf['ret'] = df_pf['r2'] - df_pf['r1']
            df_ret = pd.concat(
                [df_ret, df_pf[['portfolio', 'date', 'ret']]], axis=0)
        self.return_df = pd.merge((self.return_df), df_ret, on=[
                                  'date', 'portfolio'], how='left')
        self.return_df[['date', 'portfolio', 'day_pnl', 'night_pnl', 'total_pnl',
                        'after_fee_pnl', 'net', 'after_fee_net', 'ret']].to_csv((os.path.join(self.return_dir, 'return.csv')),
                                                                                float_format='%.6f', index=False)
        data_df = pd.read_csv(
            (os.path.join(self.return_dir, 'return.csv')), dtype={'date': str})
        data_df['date'] = data_df['date'].apply(
            lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
        if self.stat == 'on':
            if self.stat_type == 'CS':
                data_df = data_df[data_df['portfolio']
                                  == 'ValueWeighted_0.2']
                utils.assert_msg(
                    not data_df.empty, '输入的`Positon Dataframe`格式不正确，：没有portfolio = ValueWeighted_0.2的组合!')
            else:
                self._extracted_from_calc_return_(data_df)

    # TODO Rename this here and in `calc_return`
    def _extracted_from_calc_return_(self, data_df):
        if self.stat_type == 'TS':
            data_df = data_df[data_df['portfolio']
                              == 'ValueWeighted']
            utils.assert_msg(
                not data_df.empty, '输入的`Positon Dataframe`格式不正确，：没有portfolio = ValueWeighted的组合!')
        start_date = data_df['date'].iloc[0]
        end_date = data_df['date'].iloc[-1]
        x_ticks = get_first_tdates(start_date.year, end_date.year)
        f = plt.figure(figsize=(12, 24))
        gs = f.add_gridspec(4, 1)
        plt.subplots_adjust(hspace=30)
        sns.set(palette='flare')
        with sns.axes_style('whitegrid'):
            ax = f.add_subplot(gs[(0, 0)])
            ax.set_title('Cum Return Line', fontsize=24)
            plotRline(data_df, x_ticks, ax)
        sns.set(palette='Accent')
        with sns.axes_style('whitegrid'):
            ax = f.add_subplot(gs[(1, 0)])
            ax.set_title('Drawdown Line', fontsize=24)
            plotDDline(data_df, x_ticks)
        sns.set(palette='flare')
        with sns.axes_style('whitegrid'):
            ax = f.add_subplot(gs[(2, 0)])
            ax.set_title('Return Distribution', fontsize=24)
            plotRhist(data_df)
        data_df.rename(
            columns={'date': 'dates',  'net': 'nav'}, inplace=True)
        benchmarks = calc_utils.get_index()
        indicators = calc_utils.nav_statistic(
            data_df, 'all', benchmarks['zz500'], 0)
        indicators['total_ret'] = data_df['nav'].iloc[-1] - 1
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['axes.unicode_minus'] = False
        with sns.axes_style('white'):
            ax = f.add_subplot(gs[(3, 0)])
            ax.set_title('Summary', fontsize=24)
            plottext(ax, indicators, '')
        f.tight_layout()
        plt.savefig(os.path.join(
            self.return_dir, 'return_stat.png'))
        result = self.calc_nav_indicators()
        tb = calc_utils.pt.PrettyTable()
        tb.field_names = ['portfolio', 'return', 'ret_std', 'calmar',
                          'sharpe',  'max_dd',  'max_dd_date',  'fix_duration']
        for portfolio, result_dict in result.items():
            tb.add_row([portfolio, result_dict['ret'], result_dict['ret_std'], result_dict['calmar'],
                        result_dict['sharpe'], result_dict['max_dd'], result_dict['max_dd_date'], result_dict['fix_duration']])
        utils.logger.info(f'Statistic Table: \n{tb}')
