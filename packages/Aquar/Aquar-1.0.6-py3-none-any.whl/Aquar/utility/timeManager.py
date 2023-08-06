
import datetime
from . import utils
import pandas as pd
class dailyTimeManager():
    def __init__(self):
        self.start_time = ""  
        self.end_time = ""    
        self.now = self.start_time
    
    def init(self):
        start_time = utils.globalConfig['backtest']['startTime']
        end_time = utils.globalConfig['backtest']['endTime']
        data_type = utils.globalConfig['backtest']['dataType']

        start_time = datetime.datetime.strptime(start_time, '%Y%m%d %H:%M:%S.%f')
        self.start_time = utils.getCurDailyTradingTime(start_time) # floor start time
        self.end_time = datetime.datetime.strptime(end_time, '%Y%m%d %H:%M:%S.%f')    

        if self.start_time.__gt__(self.end_time):
            raise Exception(
                f'Bad config:end_time {end_time} is not later than start_time {start_time}!'
            )
        self.now = self.start_time
        utils.logger.warning("timeManager Init!")
        
    def is_start_time(self):
        return self.now == self.start_time    
      
      
    def is_end_time(self):
        return self.now >= self.end_time
    
    
    def time_forwards(self):
        self.now = utils.getNextTradingDate(self.now)      
        return self.now
        
    def set_now(self, timestamp):
        self.now = timestamp 
        
    def get_now(self):
        return self.now
    
    def get_today(self):
        return self.now.strftime('%Y-%m-%d')
    
    def get_between_time(self):
        return self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_between_year(self):
        init_year = self.start_time.year
        final_year = self.end_time.year
        return init_year,final_year
    
    
    def get_between_date(self):
        init_date = self.start_time.year*10000 +self.start_time.month*100+self.start_time.day
        if self.end_time.hour * 100 + self.end_time.minute >= 1530:
            final_date = self.end_time.year*10000 +self.end_time.month*100+self.end_time.day 
        else:
            str_final_date = self.end_time.strftime("%Y%m%d")
            final_date = int(utils.getNextTradingDate(str_final_date, -1))
        if init_date.__gt__(final_date):
            raise Exception(
                f'Bad config: init_date {init_date} is not later than final_date {final_date}'
            )
        return init_date, final_date

    def get_between_date_string(self):
        init_date = self.start_time.year*10000 + self.start_time.month*100+self.start_time.day
        if self.end_time.hour * 100 + self.end_time.minute >= 1530:
            final_date = self.end_time.year*10000 +self.end_time.month*100+self.end_time.day 
        else:
            str_final_date = self.end_time.strftime("%Y%m%d")
            final_date = int(utils.getNextTradingDate(str_final_date, -1))
        if init_date.__gt__(final_date):
            raise Exception(
                f'Bad config: init_date {init_date} is not later than final_date {final_date}'
            )
        return str(init_date), str(final_date)