from quanter import Quanter

state_up = 2
state_shake = 1
state_down = 0

THRESHOLD_DAYS = 4
THRESHOLD_DIFF_BUFFER_DAYS = 1
THRESHOLD_SAME_BUFFER_DAYS = 4

class MarketStateChecker:
    def __init__(self, records, state=state_up, last_state=state_up):
        self.records = records
        self.curr_state = [0, state]
        self.last_state = [0, last_state]
        self.high = [-1,0]
        self.low = [-1,999999999]
        self.quanter = Quanter()
        self.last_year = '2014'

    def on_day_triggered(self, day_index):

        last_record = self.records[day_index-1]
        record = self.records[day_index]
        if self.curr_state[1] == state_up:
            if record.balance > self.high[1]:
                self.high = [day_index, record.balance]
            else:
                if last_record.close < record.close:
                    if day_index - self.high[0] > THRESHOLD_DIFF_BUFFER_DAYS:
                        self.low = [day_index, record.balance]
                        self.change_state(day_index, state_shake)
                else:
                    if day_index - self.high[0] > THRESHOLD_SAME_BUFFER_DAYS:
                        self.low = [day_index, record.balance]
                        self.change_state(day_index, state_shake)
        elif self.curr_state[1] == state_down:
            if record.balance < self.low[1]:
                self.low = [day_index, record.balance]
            else:
                if last_record.close > record.close:
                    if day_index - self.low[0] > THRESHOLD_DIFF_BUFFER_DAYS:
                        self.high = [day_index, record.balance]
                        self.change_state(day_index, state_shake)
                else:
                    if day_index - self.low[0] > THRESHOLD_SAME_BUFFER_DAYS:
                        self.high = [day_index, record.balance]
                        self.change_state(day_index, state_shake)
        else:
            if self.last_state[1] == state_up:
                if record.balance < self.low[1]:
                    if day_index - self.curr_state[0] > THRESHOLD_DAYS:
                        self.low = [day_index, record.balance]
                        self.change_state(day_index, state_down)

                if record.balance > self.high[1]:
                    self.high = [day_index, record.balance]
                    self.change_state(day_index, state_up)

            elif self.last_state[1] == state_down:
                if record.balance > self.high[1]:
                    if day_index - self.curr_state[0] > THRESHOLD_DAYS:
                        self.high = [day_index, record.balance]
                        self.change_state(day_index, state_up)

                if record.balance < self.low[1]:
                    self.low = [day_index, record.balance]
                    self.change_state(day_index, state_down)
            else:
                if record.balance < self.low[1] and day_index - self.curr_state[0] > THRESHOLD_DAYS:
                    self.change_state(day_index, state_down)
                elif record.balance > self.high[1] and day_index - self.curr_state[0] > THRESHOLD_DAYS:
                    self.change_state(day_index, state_up)

                if record.balance > self.high[1]:
                    self.high = [day_index, record.balance]
                elif record.balance < self.low[1]:
                    self.low = [day_index, record.balance]

        curr_year = record.date.split("-")[0]
        if curr_year != self.last_year:
            self.quanter.on_year_change(self.last_year, curr_year, record)
            self.last_year = curr_year

    def change_state(self, day_index, state):
        self.quanter.on_market_state_change(self.curr_state[1], state, self.records[day_index + 1])
        self.last_state = self.curr_state
        self.curr_state = [day_index, state]

    def reset_low(self, day_index):
        self.low = [day_index, 999999999]

    def reset_high(self, day_index):
        self.high = [day_index, 0]

    def finish(self, day_index):
        record = self.records[day_index + 1]
        self.quanter.finish(record)