import market_state_checker

INIT_MONEY = 1000000

class Quanter:
    def __init__(self):
        self._money = INIT_MONEY
        self._stock = 0
        self._borrow = 0
        self._assets = self._money
        self._high = 0
        self._low = 9999999999
        self.year_record = [("2014", INIT_MONEY)]

    def on_market_state_change(self, old_state, new_state, next_day_record):
        open_next_day = next_day_record.open
        if new_state == market_state_checker.MARKET_STATE_UP:
            self._stock = self._money // open_next_day
            self._money -= self._stock * open_next_day
            # print("{} buy, assets = {}".format(next_day_record.date, self._assets))
        elif new_state == market_state_checker.MARKET_STATE_SHAKE:
            self.quit_market(next_day_record)
        else:
            self._borrow = self._money // open_next_day
            self._money += self._borrow * open_next_day
            # print("{} borrow".format(next_day_record.date))

    def quit_market(self, next_day_record):
        open_next_day = next_day_record.open
        if self._stock > 0:
            self._money += self._stock * open_next_day
            self._stock = 0
            # print("{} sell(quit),\t assets = {},\t win = {},\t win_rate = {}".format(next_day_record.date, self._money,
            #                                                                    self._money - self._assets, str(
            #         100 * (self._money - self._assets) / self._assets) + "%"))
        if self._borrow > 0:
            self._money -= self._borrow * open_next_day
            self._borrow = 0
            # print("{} buy(quit),\t asssets = {},\t win = {},\t win_rate = {}".format(next_day_record.date, self._money,
            #                                                                    self._money - self._assets, str(
            #         100 * (self._money - self._assets) / self._assets) + "%"))
        self._assets = self._money
        if self._assets < self._low:
            self._low = self._assets
        if self._assets > self._high:
            self._high = self._assets

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
        print("shake = {}, turnover = {}, finish, assets = {},\t win = {},\t max_fallback = {}".format(market_state_checker.THRESHOLD_SHAKE_SIGNAL, market_state_checker.THRESHOLD_TURNOVER_SIGHAL, self._assets, str(100 * (self._assets - INIT_MONEY) / INIT_MONEY) + "%", str(100 * (self._high - self._low) / self._high) + "%"))
        self._money = INIT_MONEY
        self._stock = 0
        self._borrow = 0
        self._assets = self._money
        self._high = 0
        self._low = 9999999999
        self.year_record = [("2014", INIT_MONEY)]

    def on_year_change(self, last_year, curr_year, record):
        assets = self._money
        if self._stock > 0:
            assets += self._stock * record.close

        if self._borrow > 0:
            assets -= self._borrow * record.close

        self.year_record.append((last_year,assets))