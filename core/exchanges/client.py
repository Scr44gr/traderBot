from typing import AnyStr
from core.exchanges.binance import BinanceClient


class Client:

    def __init__(self, public_key: AnyStr, secret_key: AnyStr, use_testnet=False) -> None:

        self.client = BinanceClient(public_key, secret_key, use_testnet)

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
