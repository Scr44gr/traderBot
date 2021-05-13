from typing import AnyStr, Dict, Optional,
from binance import Client
from binance.enums import SIDE_BUY, SIDE_SELL


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

        return self.__create_order(symbol=symbol, side='BUY', ord_type=order_type, price=price, **kwargs)

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
    
    def __create_test_order(self):
        
        pass
