import math


trend_down = 0
trend_shake = 1
trend_up = 2
meta_trend_days = 15
rate_threshold = 0.20

class DailyRecord:
    def __init__(self, open, close, high, low, turnover, volume):
        self.open = float(open)
        self.close = float(close)
        self.high = float(high)
        self.low = float(low)
        self.turnover = float(turnover)
        self.volume = float(volume)


target_file = open("labeled_daily_price.csv", 'w')


def get_finance_balance(path):
    with open(path, "r") as f:
        lines = f.readlines()
    result = {}
    for i in range(len(lines) - 1):
        line = lines[i]
        datas = line.split(',')
        result[datas[0]] = (datas[len(datas) - 1]).strip()
    return result

with open("daily_price.csv", "r") as src_file:
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

    finance_balance = get_finance_balance("/data/balance_origin.txt")

    # 将csv中的数据反序列化为对象
    lines.remove(lines[0])
    records = []
    for line in lines:
        words = line.strip().split(",")
        records.append(DailyRecord(words[open_ix], words[close_ix], words[high_ix], words[low_ix], words[turnover_ix], words[volume_ix]))


    # for i in range(meta_trend_days + 1, len(records)):
    for i in range(0, len(lines) - meta_trend_days + 1):
    	diff_price = records[i + meta_trend_days - 1].close - records[i].close
    	highest = 0
    	lowest = 9999999
    	for ix in range(i, i + meta_trend_days):
    		highest = max(highest, records[ix].high)
    		lowest = min(lowest, records[ix].low)
    	threshold_price = (highest - lowest) * rate_threshold
    	line = lines[i].strip()
    	if diff_price >= threshold_price:
    		target_file.write(line + "," + str(trend_up) +"\n")
    	elif diff_price <= -threshold_price:
    		target_file.write(line + "," + str(trend_down) +"\n")
    	else:
    		target_file.write(line + "," + str(trend_shake) +"\n")

target_file.close()