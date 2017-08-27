from quanter import Quanter

state_up = 2
state_shake = 1
state_down = 0

THRESHOLD_DAYS = 4
THRESHOLD_BUFFER_DAYS = 4

class MarketStateChecker:
    def __init__(self, records, state=state_up, last_state=state_up):
        self.records = records
        self.curr_state = [0, state] # curr_state[0] = 第几天变为curr_state， curr_state = [1] = state
        self.last_state = [0, last_state]  # last_state[0] = 第几天变为last_state， last_state = [1] = state
        self.high = [-1,0] # high[0] = 第几天， high[1] = 价格
        self.low = [-1,999999999] # low[0] = 第几天, low[1] = 价格
        self.quanter = Quanter()

    def on_day_triggered(self, day_index):
        '''
        根据现在的状态和新的价格，判断应该进入什么状态
        :param day_index: 市场的第day_index天
        :return: None
        '''
        last_record = self.records[day_index-1]
        record = self.records[day_index]
        if self.curr_state[1] == state_up:
            if record.balance > self.high[1]:
                self.high = [day_index, record.balance]
            else:
                if last_record.close < record.close:
                    self.low = [day_index, record.balance]
                    self.change_state(day_index, state_shake)
                else:
                    if day_index - self.high[0] > THRESHOLD_BUFFER_DAYS:
                        self.low = [day_index, record.balance]
                        self.change_state(day_index, state_shake)
        elif self.curr_state[1] == state_down:
            if record.balance < self.low[1]:
                self.low = [day_index, record.balance]
            else:
                if last_record.close > record.close:
                    self.high = [day_index, record.balance]
                    self.change_state(day_index, state_shake)
                else:
                    if day_index - self.low[0] > THRESHOLD_BUFFER_DAYS:
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