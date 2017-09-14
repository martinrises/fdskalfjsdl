from entity.OriginRecord import OriginRecord


class BalanceRecord(OriginRecord):
    def __init__(self, date, open, close, high, low, volume, turnover, balance):
        OriginRecord.__init__(self, date, open, close, high, low, volume, turnover)
        self.balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, balance):
        self.__balance = balance