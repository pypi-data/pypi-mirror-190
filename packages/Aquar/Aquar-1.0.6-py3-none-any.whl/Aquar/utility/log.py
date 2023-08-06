from . import utils
import logging  # 引入logging模块
import os.path
import time
import sys
import colorlog # 控制台日志输入颜色

log_colors_config = {'DEBUG': 'white','INFO': 'green','WARNING': 'yellow','ERROR': 'red','CRITICAL': 'bold_red'}

class LogHandler():
    def __init__(self):
        pass

    def init(self):
        logLevelDict = {'ALL':logging.NOTSET, 'DEBUG':logging.DEBUG,'INFO':logging.INFO,'WARN':logging.WARNING,'ERROR':logging.ERROR,'CRITICAL':logging.CRITICAL}
        self.fileFormatter = logging.Formatter("[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s")
        self.consoleFormatter = colorlog.ColoredFormatter('%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',log_colors=log_colors_config)
        # 第一步，创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.NOTSET)
        #创建StreamHandler对象
        sh = logging.StreamHandler(sys.stdout)
        #StreamHandler对象自定义日志级别
        logConsoleLevel = logLevelDict.get(utils.globalConfig['log']['logConsoleLevel'], logging.INFO)
        sh.setLevel(logConsoleLevel)
        #StreamHandler对象自定义日志格式
        sh.setFormatter(self.consoleFormatter)
        self.logger.addHandler(sh)  #logger日志对象加载StreamHandler对象

        # 第二步，创建一个handler，用于写入日志文件
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        log_path = f'output{os.path.sep}Logs'
        if not os.path.isdir(log_path): 
            os.makedirs(log_path)
        log_name = time.strftime("%Y%m%d_%H%M%S", time.localtime()) + '.log'
        log_file = os.path.join(log_path,log_name)
        if not os.path.isfile(log_file):  # 无文件时创建
            fd = open(log_file, mode="w", encoding="utf-8")
            fd.close()
        fh = logging.FileHandler(log_file, mode='w')
        logFileLevel = logLevelDict.get(utils.globalConfig['log']['logFileLevel'], logging.INFO)
        fh.setLevel(logFileLevel)  # 输出到file的log等级的开关

        # 第三步，定义handler的输出格式        
        fh.setFormatter(self.fileFormatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)


    def getLogHandler(self):
        return self.logger

