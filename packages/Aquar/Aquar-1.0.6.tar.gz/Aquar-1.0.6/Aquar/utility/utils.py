import datetime
import pandas as pd
import json
import re
import logging
from clickhouse_driver import Client
from . import timeManager
from . import dataEngine
from . import log

globalTimeManager = timeManager.dailyTimeManager()
globalDataEngine = dataEngine.dataEngine()
globalConfig = {}
globalReturnData = pd.DataFrame()
globalStrategyDict = {}
globalContractMap = pd.DataFrame()
globalCommodityList = []
globalLoggerHandler = log.LogHandler()
logger = logging.getLogger()


def assert_msg(condition,msg):
    if not condition:
        raise Exception(msg)

def Init():
    # loadParameters()
    globalLoggerHandler.init()
    logger = globalLoggerHandler.getLogHandler()
    globalTimeManager.init()
    globalDataEngine.init()
    
    

def Run():   
    globalDataEngine.pop_data()    


client = Client(host='10.66.200.150', port='9000',
                user='ckdb_u4', password='gtjaqh@2022')

#fetch return data from clickhoue
sql = "select formatDateTime(date,'%Y%m%d') as DATE from china_baseinfo.tradingday order by date"
result = client.execute(sql)
trading_dates = pd.DataFrame(result,columns=['DATE'])
trading_dates['DATE']=trading_dates['DATE'].astype(int)
MAX_DATE = trading_dates.iloc[-1,0]
MIN_DATE = trading_dates.iloc[0,0]
client.disconnect()

def file2date(file_name):
    return file_name.split("_")[-1][:8]

class STAT_ERROR(RuntimeError):
    def __init__(self,arg):
        self.info = arg
        
def date_range(start_date,end_date):
    for n in range(int((end_date-start_date).days)):
        yield start_date+datetime.timedelta(n)

def getAllContracts():
    pass

def extractData(regex, content, index=1): 
    p = re.compile(regex)
    return m[index] if (m := p.search(content)) else '0' 

def loadParameters(filePath = r'config.json'):
    global globalConfig
    with open(filePath,'r',encoding='utf8')as fp:
        globalConfig = json.load(fp)
    return 

def getSubscribeContract(subscribe_list):
    return subscribe_list.split(",")


def getNextTradingDate(now_time, period=1):
    if isinstance(now_time,datetime.datetime):
        int_now_time = now_time.year*10000+now_time.month*100+now_time.day
    elif isinstance(now_time, str):
        int_now_time = int(now_time)
    else:
        return -1

    result = pd.Int64Index([])
    tmp_time = now_time
    while result.empty and MIN_DATE <= int_now_time <= MAX_DATE :
        tmp_time = getNextDate(tmp_time, period)
        int_now_time = tmp_time.year*10000+tmp_time.month*100+tmp_time.day
        result = trading_dates.loc[trading_dates['DATE'] == int_now_time].index

    if result.empty:
        return -1
    idx = result[0]
    if isinstance(now_time,datetime.datetime):
        return datetime.datetime.strptime(str(trading_dates.iloc[idx]['DATE']),'%Y%m%d')
    elif isinstance(now_time, str):
        return str(trading_dates.iloc[idx]['DATE'])
    
def getCurDailyTradingTime(now_time): #find the first trading time
    int_now_time = now_time.year*10000+now_time.month*100+now_time.day
    if int_now_time > MAX_DATE: 
        return -1
    result = trading_dates.loc[trading_dates['DATE'] == int_now_time].index
    return getNextTradingDate(now_time) if result.empty else now_time  
    

def getNextDate(now_time, period=1):
    if isinstance(now_time,datetime.datetime):
        return now_time + datetime.timedelta(days = period)
    elif isinstance(now_time, str):
        ntime = datetime.datetime.strptime(now_time,"%Y%m%d")
        return ntime + datetime.timedelta(days = period)
    