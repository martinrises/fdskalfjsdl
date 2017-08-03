import pandas as pd
import numpy as np

f=open('labeled_daily_price.csv') 
df=pd.read_csv(f)     #读入股票数据
x = df.iloc[:, 1:7]
y = df.iloc[:, 7:8]

x = np.asarray(x)
y = np.asarray(y)

x = x.reshape((10, -1, 6))  # The first index changing slowest, subseries as rows
y = y.reshape((10, -1, 1)) # 将数组变形为batch_size行，总维数/行数 列的数组


print(y[0][0].shape)
