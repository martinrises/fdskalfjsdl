import math


trend_down = '0,0,1'
trend_shake = '0,1,0'
trend_up = '1,0,0'
meta_trend_days = 15
rate_threshold = 0.20
average_days = [2, 4, 8, 16, 32, 64, 128]

class DailyRecord:
    def __init__(self, date, open, close, high, low, turnover, volume):
        self.date = str(date)
        self.open = float(open)
        self.close = float(close)
        self.high = float(high)
        self.low = float(low)
        self.turnover = float(turnover)
        self.volume = float(volume)
        self.average_price = None
        self.average_vol = None

    def __str__(self):
        return '{},{},{},{},{},{},{},{},{}'.format(self.date, self.open, self.close, self.high, self.low, self.turnover, self.volume, list_to_csv_str(self.average_price), list_to_csv_str(self.average_vol))


target_file = open("./data/labeled_daily_price.csv", 'w')


def balance_str(balance):
    return str(balance) if balance != None else "0"


def get_average_price(records, i, days):
    sum_price = 0
    for record in records[i - days + 1: i + 1]:
        sum_price += record.close
    return sum_price/days


def get_average_vol(records, i, days):
    sum_vol = 0
    for record in records[i - days + 1: i + 1]:
        sum_vol += record.volume
    return sum_vol / days


def add_average_data(records):
    for i in range(average_days[-1], len(records)):
        average_prices = []
        average_vol = []
        for days in average_days:
            average_prices.append(get_average_price(records, i, days))
            average_vol.append(get_average_vol(records, i, days))
        records[i].average_price = average_prices
        records[i].average_vol = average_vol
    return records[average_days[-1]:]


def list_to_csv_str(a_list):
    csv_str = ''
    for o in a_list[:len(a_list) - 1]:
        csv_str = csv_str + str(o) + ','
    csv_str += str(a_list[-1])
    return csv_str


with open("./data/daily_price.csv", "r") as src_file:
    lines = src_file.readlines()	

    # ,open,close,high,low,total_turnover,volume
    keys = lines[0].strip().split(',')

    print(keys)
    date_ix = keys.index("")
    open_ix = keys.index("open")
    close_ix = keys.index("close")
    high_ix = keys.index("high")
    low_ix = keys.index("low")
    turnover_ix = keys.index("total_turnover")
    volume_ix = keys.index("volume")

    # 将csv中的数据反序列化为对象
    lines.remove(lines[0])
    records = []
    for line in lines:
        words = line.strip().split(",")
        date = words[date_ix]
        records.append(DailyRecord(date, words[open_ix], words[close_ix], words[high_ix], words[low_ix], words[turnover_ix], words[volume_ix]))
    records = add_average_data(records)


    # for i in range(meta_trend_days + 1, len(records)):
    for i in range(len(records) - meta_trend_days):
    	diff_price = records[i + meta_trend_days - 1].close - records[i].close
    	highest = 0
    	lowest = 9999999
    	for ix in range(i, i + meta_trend_days):
    		highest = max(highest, records[ix].high)
    		lowest = min(lowest, records[ix].low)
    	threshold_price = (highest - lowest) * rate_threshold
    	if diff_price >= threshold_price:
    		target_file.write(str(records[i]) + "," + str(trend_up) + "\n")
    	elif diff_price <= -threshold_price:
    		target_file.write(str(records[i]) + "," + str(trend_down) + "\n")
    	else:
    		target_file.write(str(records[i]) + "," + str(trend_shake) + "\n")

target_file.close()