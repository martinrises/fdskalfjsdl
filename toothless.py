import tensorflow as tf
import pandas as pd
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data
tf.set_random_seed(1)   # set random seed

# hyperparameters
lr = 0.001                  # learning rate
training_iters = 1000     # train step 上限
batch_size = 128
n_inputs = 7               # MNIST data input (img shape: 28*28)
n_steps = 1                # time steps
n_hidden_units = 28        # neurons in hidden layer
n_classes = 3              # MNIST classes (0-9 digits)

# 导入数据
f=open('./data/labeled_daily_price.csv')
df=pd.read_csv(f)     #读入股票数据
data=df.iloc[:,1:].values  #取第3-10列
data_x = data[:, :n_inputs]
data_y = data[:, n_inputs:]

# x y placeholder
x = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
y = tf.placeholder(tf.float32, [None, n_classes])

# 对 weights biases 初始值的定义
weights = {
    # shape (28, 128)
    'in': tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
    # shape (128, 10)
    'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
}
biases = {
    # shape (128, )
    'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
    # shape (10, )
    'out': tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
}

def RNN(X, weights, biases):
    # 原始的 X 是 3 维数据, 我们需要把它变成 2 维数据才能使用 weights 的矩阵乘法
    # X ==> (128 batches * 28 steps, 28 inputs)
    X = tf.reshape(X, [-1, n_inputs])

    # X_in = W*X + b
    X_in = tf.matmul(X, weights['in']) + biases['in'] # shape=[-1, n_hidden_units]
    # X_in ==> (128 batches, 28 steps, 128 hidden) 换回3维
    X_in = tf.reshape(X_in, [-1, n_steps, n_hidden_units])
    # 使用 basic LSTM Cell.
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(n_hidden_units, forget_bias=1.0, state_is_tuple=True)
    init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32)  # 初始化全零 state
    outputs, final_state = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=init_state, time_major=False)
    results = tf.matmul(final_state[1], weights['out']) + biases['out']
    return results

pred = RNN(x, weights, biases)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
train_op = tf.train.AdamOptimizer(lr).minimize(cost)

correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# 替换成下面的写法:
init = tf.global_variables_initializer()


def get_x_batch(step, batch_size):
    '''
    return data with shape = [None, n_steps, n_inputs]
    '''
    batch_xs = data_x[step * batch_size : (step + 1) * batch_size]
    result = []
    for item in batch_xs:
        temp = [None]
        temp[0] = item
        result.append(temp)
    return result


def get_y_batch(step, batch_size):
    '''
    return data with shape = [None, n_classes]
    '''
    batch_ys = data_y[step * batch_size : (step + 1) * batch_size]
    return batch_ys


with tf.Session() as sess:
    sess.run(init)

    for i in range(training_iters):
        step = 0
        cost_float = 0.
        accuracy_float = 0.
        while (step + 1) * batch_size <= len(data):
            batch_xs = get_x_batch(step, batch_size)
            batch_ys = get_y_batch(step, batch_size)
            sess.run([train_op], feed_dict={
                x: batch_xs,
                y: batch_ys,
            })

            cost_float += sess.run(cost, feed_dict={x: batch_xs, y: batch_ys})
            accuracy_float += sess.run(accuracy, feed_dict={x: batch_xs, y: batch_ys})
            step += 1
        print('step #{}, cost = {}, accuracy = {}'.format(i, cost_float/step, accuracy_float/step))
