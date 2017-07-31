target_file = open("labeled_daily_price.csv", 'w')
trend_down = 0
trend_shake = 1
trend_up = 2
meta_trend_days = 5

class DailyRecord:
    def __init__(self, open, close, high, low, turnover, volume):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.turnover = turnover
        self.volume = volume

def line2DailyRecord(line, open_ix, close_ix, high_ix, low_ix, turnover_ix, volume_ix):
    words = line.strip().split(",")
    return 

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

    # 将csv中的数据反序列化为对象
    lines.remove(lines[0])
    records = []
    for line in lines:
        words = line.strip().split(",")
        records.append(DailyRecord(words[open_ix], words[close_ix], words[high_ix], words[low_ix], words[turnover_ix], words[volume_ix]))

