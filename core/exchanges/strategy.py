from time import sleep
from logging import getLogger
from os import getenv

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
            sleep(int(getenv('STRATEGY_PROCESS_SLEEP_TIME')))

            try:
                self.strategy()
            except:
                self.__logger.error(
                    "An error has ocurred on self.strategy func, details: ", exc_info=1)
                if int(getenv('BREAK_STRATEGY_PROCESS', 0)):
                    break

    @property
    def name(self, value):
        self._name = value

    @name.setter
    def name(self):
        return self._name
