
from . import utils
from ..subDataEngine import dataLoaderDaily

class dataEngine():
    def init(self):
        self.data_type = utils.globalConfig['backtest'].get('dataType','DAILY')
        if self.data_type == 'DAILY':
            self.sub_engine = dataLoaderDaily.dataEngine()
        self.sub_engine.init()

    def pop_data(self):
        self.sub_engine.pop_data()    

            
            

