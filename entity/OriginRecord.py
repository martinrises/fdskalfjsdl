class OriginRecord:
    def __init__(self, date, open, close, high, low, volume, turnover):
        self.date = date
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.turnover = turnover

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def open(self):
        return self.__open

    @open.setter
    def open(self, open):
        self.__open = open

    @property
    def close(self):
        return self.__close

    @close.setter
    def close(self, close):
        self.__close = close

    @property
    def high(self):
        return self.__high

    @high.setter
    def high(self, high):
        self.__high = high

    @property
    def low(self):
        return self.__low

    @low.setter
    def low(self, low):
        self.__low = low

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, volume):
        self.__volume = volume

    @property
    def turnover(self):
        return self.__turnover

    @turnover.setter
    def turnover(self, turnover):
        self.__turnover = turnover