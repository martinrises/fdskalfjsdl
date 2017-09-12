import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd

f=open('./data/labeled_daily_price.csv')
df=pd.read_csv(f)
y=df.iloc[:,7].values

print(y[0:10])

data = list(zip(range(len(y)), y))

data = tf.unstack(data, axis=1)
data = tf.Session().run(data)

plt.plot(data[0],data[1])
plt.show()