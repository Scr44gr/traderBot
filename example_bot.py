from core.exchanges.client import Client
from core.indicators.supertrend import Supertrend
from core.utils import override, safe_number
from dotenv import load_dotenv, find_dotenv
from os import getenv
import logging

logging.basicConfig(format='[%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

class BotStrategy(Client):

    def __init__(self, indicator) -> None:
        super().__init__(public_key=getenv('PUBLIC_KEY'), secret_key=getenv('SECRET_KEY'), use_testnet=getenv('TESTNET'))

        self.logger = logging.getLogger('Strategy')
        self.symbol = getenv('SYMBOL')
        self.indicator = indicator
        self.indicator.set_klines_func(self.client.get_klines)

    @property
    def prev_asks_price(self):

        return self._prev_asks_price + (self._prev_asks_price * getenv('ASKS_MARGIN_PERCENTAGE', 0))

    @property
    def prev_bids_price(self):

        return self._prev_bids_price + (self._prev_asks_price * getenv('BIDS_MARGIN_PERCENTAGE', 0))

    @override
    def strategy(self):
        self.indicator.start()

    def on_buy_handler(self):
        self.logger.info('Buying...')
        self.clear_open_orders(self.symbol, 'BUY')

        if self.is_available_balance(self.symbol):
            price = self.get_asks_price(self.symbol)
            quantity = (safe_number(self.balance) * (float(getenv('BALANCE_TO_USE', 0.99)) / safe_number(self.get_asks_price(self.symbol))))
            quantity = self.to_exact_precision(self.symbol, quantity)
            order = self.create_buy_order(symbol=self.symbol, order_type="LIMIT", price=price, quantity=quantity)
            self.logger.info(f'Buy order executed! ORDER_ID: {order["orderId"]} STATUS: {order["status"]} ')

    def on_sell_handler(self):
        self.logger.info('Selling...')
        self.clear_open_orders(self.symbol, 'SELL')

        if self.is_available_balance(self.symbol):
            price = self.get_bids_price(self.symbol)
            quantity = (safe_number(self.balance) * (float(getenv('BALANCE_TO_USE', 0.99)) / safe_number(self.get_asks_price(self.symbol))))
            quantity = self.to_exact_precision(self.symbol, quantity)
            order = self.create_sell_order(symbol=self.symbol, order_type="LIMIT", price=price, quantity=quantity)
            self.logger.info(f'Sell order executed! ORDER_ID: {order["orderId"]} STATUS: {order["status"]} ')

    def set_up_handlers(self):

        self.indicator.add_event_handler('uptrend', self.on_buy_handler)
        self.indicator.add_event_handler('downtrend', self.on_sell_handler)

if __name__ == "__main__":

    load_dotenv(find_dotenv(), override=True)
    supertrend = Supertrend()
    
    bot = BotStrategy(indicator = supertrend)
    bot.set_up_handlers()
    bot.run()