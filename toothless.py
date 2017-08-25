import tensorflow as tf
import pandas as pd
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data
tf.set_random_seed(1)   # set random seed

# hyperparameters
lr = 0.001                 # learning rate
training_iters = 10000      # train step 上限
batch_size = 100
n_inputs = 14              # MNIST data input (img shape: 28*28)
n_hidden_units = 20        # neurons in hidden layer
n_hidder_layers = 2        # 隐藏层的参数
n_classes = 3              # MNIST classes (0-9 digits)

# 导入数据
f=open('./data/labeled_daily_price.csv')
df=pd.read_csv(f)
data=df.iloc[:,1:].values  #取第3-10列
data_x = data[:, :n_inputs]
data_y = data[:, n_inputs:]

input = tf.placeholder(dtype=tf.float32, shape=[None, n_inputs])
target = tf.placeholder(dtype=tf.int32, shape=[None, n_classes])

input_W = tf.Variable(tf.zeros(shape=[n_inputs, n_hidden_units]))
input_b = tf.Variable(tf.zeros(shape=[n_hidden_units]))
output0 = tf.matmul(input, input_W) + input_b

# Define Variable Functions (weights and bias)
def init_weight(shape):
    weight = tf.Variable(tf.zeros(shape))
    return (weight)

def init_bias(shape):
    bias = tf.Variable(tf.zeros(shape))
    return (bias)

# Create a fully connected layer:
def fully_connected(input_layer, weights, biases):
    layer = tf.add(tf.matmul(input_layer, weights), biases)
    return (tf.nn.relu(layer))

def add_hidder_layer(input):
    W = init_weight(shape=[n_hidden_units, n_hidden_units])
    b = init_bias(shape=[n_hidden_units, 1])
    layer = tf.add(tf.matmul(input, W), b)
    return (tf.nn.relu(layer))


def stack_hidden_layer(input):
    output_temp = input
    for _ in range(n_hidder_layers - 1):
        output_temp = add_hidder_layer(output_temp)
    return output_temp


hidden_output = stack_hidden_layer(output0)
output_W = tf.Variable(tf.zeros(shape=[n_hidden_units, n_classes]))
outut_b = tf.Variable(tf.zeros(shape=[n_classes]))
output = tf.matmul(output0, output_W) + outut_b

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=target, logits=output))

correct_prediction = tf.equal(tf.argmax(output,1), tf.argmax(target,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

train_step = tf.train.AdamOptimizer(lr).minimize(cross_entropy)

with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    optimizer = tf.train.GradientDescentOptimizer(lr)
    for epoch in range(training_iters):
        for i in range((len(data_x) // batch_size) - 1):
            actual_x = data_x[i * batch_size: (i + 1) * batch_size, :]
            actual_y = data_y[i * batch_size: (i + 1) * batch_size, :]
            sess.run(train_step, feed_dict={input:actual_x, target: actual_y})

        output_actual = sess.run(output, feed_dict={input: actual_x, target: actual_y})
        print("epoch #{}, cost = {}, accuracy = {}".format(epoch, sess.run(cross_entropy, feed_dict={input:actual_x, target: actual_y}), sess.run(accuracy, feed_dict={input:actual_x, target: actual_y})))