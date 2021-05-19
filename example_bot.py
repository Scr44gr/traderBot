from typing import AnyStr
from core.exchanges.client import Client
from os import getenv
import logging
from dotenv import load_dotenv, find_dotenv

class BotStrategy(Client):

    def __init__(self) -> None:
        super().__init__(public_key=getenv('PUBLIC_KEY'), secret_key=getenv('SECRET_KEY'), use_testnet=getenv('TESTNET'))

        self.logger = logging.getLogger('Strategy')
        self.logger.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

        self.analyze_symbols = ['LTCBTC']

    @property
    def prev_asks_price(self):

        return self._prev_asks_price + (self._prev_asks_price * getenv('ASKS_MARGIN_PERCENTAGE', 0))

    @property
    def prev_bids_price(self):

        return self._prev_bids_price + (self._prev_asks_price * getenv('BIDS_MARGIN_PERCENTAGE', 0))

    def strategy(self):
        
        pass
    
    def analyzer(self):

        for symbol in self.analyze_symbols:
            if self.get_asks_price(symbol) <= self.prev_asks_price:
                self.logger.info("BUYING OPPORTUNITY!")
            
            if self.get_bids_price(symbol) < self.prev_bids_price:
                self.logger.info("SELLING OPPORTUNITY!")


if __name__ == "__main__":

    load_dotenv(find_dotenv(), override=True)