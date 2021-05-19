from time import sleep
from logging import getLogger


class Strategy:

    def __init__(self) -> None:
        self.process = True
        self.orders = []
        self._prev_asks_price = 0
        self._prev_bids_price = 0

        self.__logger = getLogger('Strategy')

    def strategy(self): ...

    def run(self) -> None:
        self.__logger.info("STRATEGY STARTED")
        while self.process:
            try:
                self.strategy()
                sleep(1)
            except:
                self.__logger.error(
                    "An error has ocurred on self.strategy func, details: ", exc_info=1)
                break
