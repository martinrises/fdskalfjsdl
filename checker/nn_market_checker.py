import numpy as np

from checker.quanter import Quanter


class NnMarketChecker:

    def __init__(self, records):
        self.records = records
        self.__state = 1 # {0:up, 1:shake, 2:down}
        self.__quanter = Quanter()
        self.__right_cnt = 0
        self.__curr_year = self.records[0].year

    @property
    def records(self):
        return self.__records

    @records.setter
    def records(self, records):
        self.__records = records

    @property
    def state(self):
        return self.__state

    def on_day_triggerd(self, index, prediction):
        new_state = np.argmax(prediction)

        # accuracy
        target = np.argmax(self.records[index].label)
        if target ==  new_state:
            self.__right_cnt += 1

        # state
        if new_state != self.state:
            self.__quanter.on_market_state_change(self.state, new_state, self.records[index+1])
            self.__state = new_state

        # year
        year = self.records[index].year
        if year != self.__curr_year:
            self.__quanter.on_year_change(self.__curr_year, year, self.records[index])
            self.__curr_year = year

    def finish(self, day_index):
        record = self.records[day_index + 1]
        self.__quanter.finish(record)
        print("accuracy = {}%".format(self.__right_cnt * 100 / len(self.records)))