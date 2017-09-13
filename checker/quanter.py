
INIT_MONEY = 1000000
MARKET_STATE_UP = 0
MARKET_STATE_SHAKE = 1
MARKET_STATE_DOWN = 2

class Quanter:
    def __init__(self):
        self.money = INIT_MONEY
        self.stock = 0
        self.borrow = 0
        self.high = 0
        self.low = 9999999999
        self.year_record = [("0000", INIT_MONEY)]
        self._start_assets = 0

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, money):
        self.__money = money

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, stock):
        self.__stock = stock

    @property
    def borrow(self):
        return self.__borrow

    @borrow.setter
    def borrow(self, borrow):
        self.__borrow = borrow

    def assets(self, close):
        return self.money + self.stock * close - self.borrow * close


    def on_market_state_change(self, old_state, new_state, next_day_record):
        if old_state == new_state:
            return

        if abs(old_state - new_state) == 2:
            self.quit_market(next_day_record)

        open_next_day = next_day_record.open
        if new_state == MARKET_STATE_UP:
            stock = self.money // open_next_day
            self.stock += stock
            self.money -= stock * open_next_day
            self._start_assets = self.assets(open_next_day)
            print("{} buy, assets = {}".format(next_day_record.date, self.assets(open_next_day)))
        elif new_state == MARKET_STATE_SHAKE:
            self.quit_market(next_day_record)
            print("{} shake, assets = {}".format(next_day_record.date, self.assets(open_next_day)))
        else:
            borrow = self.money // open_next_day
            self.borrow += borrow
            self.money += borrow * open_next_day
            self._start_assets = self.assets(open_next_day)
            print("{} borrow, assets = {}".format(next_day_record.date, self.assets(open_next_day)))

    def quit_market(self, next_day_record):
        open_next_day = next_day_record.open
        if self.stock > 0:
            self.money += self.stock * open_next_day
            self.stock = 0
        if self.borrow > 0:
            self.money -= self.borrow * open_next_day
            self.borrow = 0
        self._start_assets = 0

    def finish(self, next_day_record):
        self.quit_market(next_day_record)
        self.on_year_change("2017", "2018",next_day_record)
        for i in range(len(self.year_record)):
            assets_record = self.year_record[i]
            last_index = 0
            if i > 0:
                last_index = i - 1
            start_assets = self.year_record[last_index][1]
            end_assets = self.year_record[i][1]
            print("{}, start_assets = {}, end_assets = {}, win_rate = {}".format(
                assets_record[0],
                start_assets,
                end_assets,
                str(100 * (end_assets - start_assets) / start_assets) + "%"
            ))
        print(" finish, assets = {},\t win = {}".format(self.assets(next_day_record.open), str(100 * (self.assets(next_day_record.open) - INIT_MONEY) / INIT_MONEY) + "%"))

    def on_year_change(self, last_year, curr_year, record):
        self.year_record.append((last_year, self.assets(record.close)))

    def on_day_trigger(self, curr_record, next_record):
        if self._start_assets != 0 and (self.assets(curr_record.close) - self._start_assets) / self._start_assets < -0.03:
            print("wrong operation, loss = {}".format((self.assets(curr_record.close) - self._start_assets) / self._start_assets))
            self.quit_market(next_record)
