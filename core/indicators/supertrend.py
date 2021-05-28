from core.utils import override
from os import getenv
from core.indicators import Indicator
from logging import getLogger
import pandas as pd
pd.set_option('display.max_rows', None)

class Supertrend(Indicator):

    def __init__(self):
        super().__init__()
        self.__logger = getLogger('SupertrendIndicator')
        self._in_position = False

    def buy_signal(self, f):
        self.__logger.info('UPTREND, BUYING...')

    def sell_signal(self):
        self.__logger.info('DOWNTREND, SELLING...')

    def indicator(self, dataframe, period=7, atr_multiplier=3):
        """
        SuperTrend.
        """
        hl2 = (dataframe['high'] + dataframe['low']) / 2
        dataframe['atr'] = self.atr(dataframe, period)
        dataframe['upperband'] = hl2 + (atr_multiplier * dataframe['atr'])
        dataframe['lowerband'] = hl2 - (atr_multiplier * dataframe['atr'])
        dataframe['uptrend'] = True

        return self.supertrend(dataframe)

    @staticmethod
    def supertrend(dataframe):
        data_lenght = len(dataframe.index)
        for current in range(1, data_lenght):
            previous = current - 1

            if dataframe['close'][current] > dataframe['upperband'][previous]:
                dataframe['uptrend'][current] = True
            elif dataframe['close'][current] < dataframe['lowerband'][previous]:
                dataframe['uptrend'][current] = False
            else:
                dataframe['uptrend'][current] = dataframe['uptrend'][previous]

                if dataframe['uptrend'][current] and dataframe['lowerband'][current] < dataframe['lowerband'][previous]:
                    dataframe['lowerband'][current] = dataframe['lowerband'][previous]
                
                if not dataframe['uptrend'][current] and dataframe['upperband'][current] > dataframe['upperband'][previous]:
                    dataframe['upperband'][current] = dataframe['upperband'][previous]
        return dataframe
    
    def check_signal(self, dataframe):
        self.__logger.info("Checking buy/sell signal..")
        
        current = len(dataframe.index) - 1
        previous = current - 1
        if not dataframe['uptrend'][previous] and dataframe['uptrend'][current]:
            self.__logger.debug('Uptrend, buying..')
            if self._in_position:
                self.__logger.debug('Already in position.')
                return
            
            self.call_event('uptrend')
            self._in_position = True

        if dataframe['uptrend'][previous] and not dataframe['uptrend'][current]:
            self.__logger.debug('Downtrend, selling..')
            if not self._in_position:
                self.__logger.debug('Not in position.')
                return
            
            self.call_event('downtrend')
            self._in_position = False

    def start(self):

        self.__logger.debug('On fetching new candles')
        
        INTERVAL = getenv('INTERVAL', '1m')
        LIMIT = int(getenv('LIMIT', 100))

        candles = self.get_klines(getenv('SYMBOL'), interval=INTERVAL, limit=LIMIT, parse_data=True)
        dataframe = pd.DataFrame(candles[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit='ms')

        data = self.indicator(dataframe)
        self.check_signal(data)
        
