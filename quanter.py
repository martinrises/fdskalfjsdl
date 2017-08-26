import market_state_checker

init_money = 1000000

class Quanter:
    def __init__(self):
        self._money = init_money
        self._stock = 0 # 借的股票
        self._borrow = 0 # 买的股票
        self._assets = self._money
        self._high = 0
        self._low = 9999999999

    def on_market_state_change(self, old_state, new_state, next_day_record):
        open_next_day = next_day_record.open
        if new_state == market_state_checker.state_up:
            self._stock = self._money // open_next_day# 把钱都换成股票
            self._money -= self._stock * open_next_day
            print("{} buy, assets = {}".format(next_day_record.date, self._assets))
        elif new_state == market_state_checker.state_shake:
            self.quit_market(next_day_record)
        else:
            self._borrow = self._money // open_next_day
            self._money += self._borrow * open_next_day
            print("{} borrow".format(next_day_record.date))

    def quit_market(self, next_day_record):
        '''
        平仓
        '''
        open_next_day = next_day_record.open
        if self._stock > 0:
            self._money += self._stock * open_next_day
            self._stock = 0
            print("{} sell(quit),\t assets = {},\t win = {},\t win_rate = {}".format(next_day_record.date, self._money,
                                                                               self._money - self._assets, str(
                    100 * (self._money - self._assets) / self._assets) + "%"))
        if self._borrow > 0:
            self._money -= self._borrow * open_next_day
            self._borrow = 0
            print("{} buy(quit),\t asssets = {},\t win = {},\t win_rate = {}".format(next_day_record.date, self._money,
                                                                               self._money - self._assets, str(
                    100 * (self._money - self._assets) / self._assets) + "%"))
        self._assets = self._money
        if self._assets < self._low:
            self._low = self._assets
        if self._assets > self._high:
            self._high = self._assets

    def finish(self, next_day_record):
        self.quit_market(next_day_record)
        print("finish, assets = {},\t win = {},\t max_fallback = {}".format(self._assets,  str(100 * (self._assets - init_money)/ init_money) + "%", str(100 * (self._high - self._low)/self._high) + "%"))