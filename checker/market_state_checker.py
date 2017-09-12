from checker.quanter import Quanter

MARKET_STATE_UP = 2
MARKET_STATE_SHAKE = 1
MARKET_STATE_DOWN = 0

THRESHOLD_SHAKE_SIGNAL = 4
THRESHOLD_TURNOVER_SIGHAL = 4

BALANCE_EVENT_UP = 2
BALANCE_EVENT_SHAKE = 1
BALANCE_EVENT_DOWN = 0

SIGNAL_STRONG = 4
SIGNAL_NORMAL = 2
SIGNAL_LIGHT = 1

INIT_HIGH = 0
INIT_LOW = 9999999999999999

class MarketStateChecker:
    def __init__(self, records):
        self.records = records
        self.curr_market_state = MARKET_STATE_UP
        self.last_market_state = MARKET_STATE_UP
        self.high = INIT_HIGH
        self.low = INIT_LOW
        self.last_year = '2014'
        self.change_signal = []
        self.quanter = Quanter()

    def on_day_triggered(self, day_index):
        last_record = self.records[day_index - 1 if day_index > 0 else day_index]
        curr_record = self.records[day_index]
        self.high, self.low, balance_event = self.trigger_balance_event(day_index)

        signal = self.get_signal(balance_event, curr_record.close > last_record.close)
        self.change_signal.append(signal)
        next_market_state = self.check_market_state()

        if not next_market_state == self.curr_market_state:
            if next_market_state == MARKET_STATE_DOWN:
                self.hign = INIT_HIGH
            elif next_market_state == MARKET_STATE_UP:
                self.low = INIT_LOW
            self.last_market_state = self.curr_market_state
            self.curr_market_state = next_market_state
            self.quanter.on_market_state_change(self.last_market_state, self.curr_market_state, self.records[day_index + 1])

        curr_year = curr_record.date.split("-")[0]
        if curr_year != self.last_year:
            self.quanter.on_year_change(self.last_year, curr_year, curr_record)
            self.last_year = curr_year

    def trigger_balance_event(self, day_index):
        '''
        input : curr_record.balance, high, low
        output: high, low, balance_event_type
        '''
        high = self.high
        low = self.low
        balance_event = BALANCE_EVENT_SHAKE

        curr_balance = self.records[day_index].balance

        if low == INIT_LOW:
            if curr_balance > high:
                high = curr_balance
                balance_event = BALANCE_EVENT_UP
            else:
                low = curr_balance
                balance_event = BALANCE_EVENT_DOWN
        elif high == INIT_HIGH:
            if curr_balance < low:
                low = curr_balance
                balance_event = BALANCE_EVENT_DOWN
            else:
                high = curr_balance
                balance_event = BALANCE_EVENT_UP
        else:
            if curr_balance > high:
                high = curr_balance
                balance_event = BALANCE_EVENT_UP
            elif curr_balance < low:
                low = curr_balance
                balance_event = BALANCE_EVENT_DOWN
            else:
                balance_event = BALANCE_EVENT_SHAKE

        return high, low, balance_event



    def finish(self, day_index):
        record = self.records[day_index + 1]
        self.quanter.finish(record)

    def get_signal(self, balance_event, is_price_up):
        '''
        input : balance_event, is_price_up, curr_market_state
        output: signal
        '''
        signal = SIGNAL_NORMAL
        curr_market_state = self.curr_market_state
        if curr_market_state == MARKET_STATE_DOWN:
            if balance_event == BALANCE_EVENT_DOWN:
                signal = -SIGNAL_NORMAL
            elif balance_event == BALANCE_EVENT_UP:
                signal = SIGNAL_STRONG if is_price_up else SIGNAL_NORMAL
            else:
                signal = SIGNAL_NORMAL if is_price_up else SIGNAL_LIGHT
        elif curr_market_state == MARKET_STATE_UP:
            if balance_event == BALANCE_EVENT_UP:
                signal = SIGNAL_NORMAL
            elif balance_event == BALANCE_EVENT_DOWN:
                signal = -SIGNAL_STRONG if not is_price_up else -SIGNAL_NORMAL
            else:
                signal = -SIGNAL_NORMAL if not is_price_up else -SIGNAL_LIGHT
        else:
            if balance_event == BALANCE_EVENT_UP:
                signal = SIGNAL_STRONG if is_price_up else SIGNAL_NORMAL
            elif balance_event == BALANCE_EVENT_DOWN:
                signal = -SIGNAL_STRONG if not is_price_up else -SIGNAL_NORMAL
            else:
                signal = SIGNAL_LIGHT if is_price_up else -SIGNAL_LIGHT
        return signal

    def check_market_state(self):
        '''
        input : self.change_signal, self.curr_market_state
        output: next_market_state
        '''
        change_signal_sum = sum(self.change_signal)
        curr_market_state = self.curr_market_state
        next_market_state = self.curr_market_state

        if curr_market_state == MARKET_STATE_UP:
            # if change_signal_sum < 0:
                # print("UP ######   change_signal_sum = {}".format(change_signal_sum))
            if change_signal_sum > 0:
                self.change_signal.clear()
            elif change_signal_sum < -THRESHOLD_SHAKE_SIGNAL:
                next_market_state = MARKET_STATE_SHAKE
        elif curr_market_state == MARKET_STATE_DOWN:
            # if change_signal_sum > 0:
                # print("DOWN @@@@@@@ change_signal_sum = {}".format(change_signal_sum))
            if change_signal_sum < 0:
                self.change_signal.clear()
            elif change_signal_sum > -THRESHOLD_SHAKE_SIGNAL:
                next_market_state = MARKET_STATE_SHAKE
        else:
            # print("SHAKE ~~~~~~~~   change_signal_sum = {}".format(change_signal_sum))
            if change_signal_sum > THRESHOLD_TURNOVER_SIGHAL:
                next_market_state = MARKET_STATE_UP
            elif change_signal_sum < -THRESHOLD_TURNOVER_SIGHAL:
                next_market_state = MARKET_STATE_DOWN
        return next_market_state