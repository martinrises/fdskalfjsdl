import matplotlib.pyplot as plt
import tensorflow as tf

DAYS = 60

class DailyRecord:
    def __init__(self, date, open, close, high, low, turnover, volume, balance):
        self.date = str(date)
        self.open = float(open)
        self.close = float(close)
        self.high = float(high)
        self.low = float(low)
        self.turnover = float(turnover)
        self.volume = float(volume)
        self.balance = balance


def get_finance_balance(path):
    with open(path, "r") as f:
        lines = f.readlines()
        result = {}
        for i in range(len(lines) - 1):
            line = lines[i]
            datas = line.split(',')
            result[datas[0]] = float((datas[-1]).strip())
        return result


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

    finance_balance = get_finance_balance("./data/balance_origin.txt")

    # 将csv中的数据反序列化为对象
    lines.remove(lines[0])
    records = []
    for line in lines:
        words = line.strip().split(",")
        date = words[date_ix]
        records.append(DailyRecord(date, words[open_ix], words[close_ix], words[high_ix], words[low_ix], words[turnover_ix], words[volume_ix], finance_balance.get(date)))

    records = records[-len(finance_balance):]

data_price = list(zip(range(len(records)), [r.close for r in records]))
data_price = data_price[-1:-DAYS:-1]
data_price = tf.unstack(data_price, axis=1)
with tf.Session() as sess:
    data_price = sess.run(data_price)

balance = []
for r in records:
    if not r.balance == None:
        balance.append(r.balance/200000000 * 3/4)
    else:
        balance.append(0)

data_balance = list(zip(range(len(records)), balance))
data_balance = data_balance[-1:-DAYS:-1]
data_balance = tf.unstack(data_balance, axis=1)
with tf.Session() as sess:
    data_balance = sess.run(data_balance)


plt.plot(data_price[0],data_price[1])
plt.plot(data_balance[0],data_balance[1])
plt.show()