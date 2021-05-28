from typing import AnyStr, Dict, List, Optional
from binance import Client
from binance.enums import SIDE_BUY, SIDE_SELL
from core.utils import safe_number

class BinanceClient:

    def __init__(self, public_key: Optional[AnyStr] = None, secret_key: Optional[AnyStr] = None, use_testnet=False) -> None:

        self._api = Client(public_key, secret_key, testnet=use_testnet)

    def create_buy_order(self, **kwargs) -> Dict:
        """
        :params:

        - symbol <str>
        - order_type <str>
        - price <str>
        - quantity <[float, decimal]>

        """
        symbol = kwargs.pop('symbol')
        order_type = kwargs.pop('order_type')
        quantity = kwargs.pop('quantity')
        price = kwargs.pop('price')

        if kwargs.pop('test_order'):
            return self.__create_test_order(symbol=symbol, side=SIDE_BUY, order_type=order_type, quantity=quantity, price=price)

        return self.__create_order(symbol=symbol, side=SIDE_BUY, ord_type=order_type, price=price, **kwargs)

    def create_sell_order(self, **kwargs) -> Dict:
        """
        :params:

        - symbol <str>
        - order_type <str>
        - price <str>
        - quantity <[float, decimal]>

        """
        symbol = kwargs.pop('symbol')
        order_type = kwargs.pop('order_type')
        quantity = kwargs.pop('quantity')
        price = kwargs.pop('price')


        if kwargs.pop('test_order'):
            return self.__create_test_order(symbol=symbol, side=SIDE_SELL, order_type=order_type, quantity=quantity, price=price)

        return self.__create_order(symbol=symbol, side=SIDE_SELL, ord_type=order_type, price=price, **kwargs)

    def __create_order(self, symbol, side, ord_type, quantity, price, **kwargs) -> Dict:

        return self._api.create_order(symbol=symbol, side=side, type=ord_type, quantity=quantity, price=price, **kwargs)
    
    def __create_test_order(self, symbol, side, ord_type, quantity, price, **kwargs) -> Dict:
        
        return self._api.create_test_order(symbol=symbol, side=side, type=ord_type, quantity=quantity, price=price, **kwargs)
    
    def get_bids_price(self, symbol):

        return float(self._api.get_order_book(symbol)['bids'][0][0])
    
    def get_asks_price(self, symbol):
        
        return float(self._api.get_order_book(symbol)['asks'][0][0])
    
    def get_open_orders(self) -> List[Dict]:

        return self._api.get_open_orders()
    
    def cancel_order(self, symbol, order_id):

        return self._api.cancel_order(symbol, order_id)
    
    def get_klines(self, symbol, interval, limit=500, **kwargs):

        data = self._api.get_klines(symbol=symbol, interval=interval, limit=limit)
        if kwargs.pop('parse_data', 0):
            parsed_data = []
            for column in data:
                parsed_data.append(self._parse_klines(column))
            return parsed_data
        return data

    @staticmethod
    def _parse_klines(data):

        response = []

        for i in range(0, 6):
            response.append(safe_number(data[i]))

        return response


