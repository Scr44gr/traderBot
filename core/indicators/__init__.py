from core.utils import EventHandler

class Indicator(EventHandler):

    def __init__(self):
        super().__init__()
    
    def set_klines_func(self, value):
        self.klines_func = value

    @staticmethod
    def tr(dataframe):
        """
        True Range | TR
        """
        dataframe['prev-close'] = dataframe['close'].shift(1)
        dataframe['high-low'] = abs(dataframe['high'] - dataframe['low'])
        dataframe['high-pc'] = abs(dataframe['low'] - dataframe['prev-close'])
        dataframe['low-pc'] = abs(dataframe['low'] - dataframe['prev-close'])

        tr = dataframe[['high-low', 'high-pc', 'low-pc']].max(axis=1)

        return tr

    def atr(self, dataframe, period):
        """
        Average True Range | ATR
        """
        dataframe['tr'] = self.tr(dataframe)
        atr = dataframe['tr'].rolling(period).mean()
        return atr

    def get_klines(self, symbol, interval='1m', limit=100, **kwargs):
        
        return self.klines_func(symbol, interval, limit, **kwargs)
    
