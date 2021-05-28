from typing import AnyStr, List
from core.exchanges.binance import BinanceClient
from core.exchanges.strategy import Strategy
from logging import getLogger
from core.utils import safe_number

class Client(Strategy):

    def __init__(self, public_key: AnyStr, secret_key: AnyStr, use_testnet=False) -> None:
        super().__init__()
        
        self.__logger = getLogger('Client')
        self.balance = ''
        if (public_key and secret_key) is not None:
            self.client = BinanceClient(public_key, secret_key, use_testnet)
        else:
            raise Exception('API KEYS ERROR, PLEASE CHECK AND RUN THE CLIENT AGAIN!')

    def create_buy_order(self, **kwargs):
        """
        CREATE A NEW BUY ORDER

        :params:

        - symbol <str>
        - order_type <str>
        - price <str>
        - quantity <[float, decimal]>

        """
        return self.client.create_buy_order(**kwargs)

    def create_sell_order(self, **kwargs):
        """
        CREATE A NEW SELL ORDER

        :params:

        - symbol <str>
        - order_type <str>
        - price <str>
        - quantity <[float, decimal]>

        """
        return self.client.create_sell_order(**kwargs)

    def create_buy_test_order(self, **kwargs):
        """
        CREATE A NEW BUY TEST ORDER

        :params:

        - symbol <str>
        - order_type <str>
        - price <str>
        - quantity <[float, decimal]>

        """
        return self.client.create_buy_order(test_order=True, **kwargs)

    def create_sell_test_order(self, **kwargs):
        """
        CREATE A NEW SELL TEST ORDER

        :params:

        - symbol <str>
        - order_type <str>
        - price <str>
        - quantity <[float, decimal]>

        """
        return self.client.create_sell_order(test_order=True, **kwargs)

    def get_bids_price(self, symbol: AnyStr) -> float:
        """
        GET THE ACTUAL BIDS PRICE.


        :params:

        - symbol <str>
        """

        self._prev_bids_price = self.client.get_bids_price(symbol)
        return self._prev_bids_price

    def get_asks_price(self, symbol: AnyStr) -> float:
        """
        GET THE ACTUAL ASKS PRICE.


        :params:

        - symbol <str>
        """

        self._prev_asks_price = self.client.get_asks_price(symbol)
        return self._prev_asks_price

    def get_open_orders(self) -> List:
        """
        GET A LIST OF OPEN ORDERS.
        """

        return self.client.get_open_orders()

    def cancel_order(self, symbol, order_id):
        """
        CANCELS AN OPEN ORDER.
        
        :params:

        - symbol <str>
        - order_id <str>

        """
        return self.client.cancel_order(symbol, order_id)
    
    def get_klines(self, symbol, interval, limit, **kwargs):
        """
        Get Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
        
        :params:
        
        - symbol <str>
        - limit <int> default 500, max 1500 for futures, max 1000 for spot markets.
        - startTime <int> optional
        - endTime <int> optional

        """
        
        return self.client.get_klines(symbol, interval, limit, **kwargs)
    
    def __get_symbol_info(self, symbol):
        """Private func to get the symbol info.

        :params:
        - symbol <str>

        """
        return self.client._api.get_symbol_info(symbol)

    def clear_open_orders(self, symbol, side):
        """Check for open orders and cancel it.

        :params:
        - symbol <str> 
        - side <str> BUY - SELL
        """
        self.__logger.debug('Cleaning open orders..')

        for order in self.get_open_orders():
            if order['symbol'] == symbol and order['side'] == side:
                try:
                    response = self.cancel_order(self.symbol, order['orderId'])
                    self.__logger.info(f'Order {response["id"]} cancelled')
                except:
                    self.__logger.error('An error occurred while trying to cancel the order. details:', exc_info=1)
    
    def is_available_balance(self, symbol):
        """Check in the current balance is available to make an order.

        :params:
        - symbol <str>
        """
        symbol_info = self.__get_symbol_info(symbol)
        response = self.client.get_current_asset_balance(symbol_info['baseAsset'])
        balance = response['free']
        is_available = safe_number(balance) > safe_number(symbol_info['filters'][0]['minPrice'])

        return is_available
    
    def to_exact_precision(self, symbol, quantity):
        """Check the quantity precision and return the exact.

        :params:
        - symbol <str>
        - quantity <str|float|int>
        """
        symbol_info = self.__get_symbol_info(symbol)
        lot_size_fix = 3
        precision = safe_number(symbol_info['baseAssetPrecision']) - lot_size_fix

        return f'{quantity:.{precision}f}'