import origin_data_reader
import labeler
import tensorflow as tf
import numpy as np

DAYS = 2
FEATURE_SIZE = 6
n_input = FEATURE_SIZE * DAYS
THRESHOLD = 0.02
n_label = 3
n_hidden_unit = 50
learning_rate = 0.001
batch_size = 30
max_epoch = 1000


def get_features(labeled_records):
    features = []
    for record in labeled_records:
        features.append([record.features])
    return features


def get_labels(labeled_records):
    labels = []
    for record in labeled_records:
        labels.append([record.label])
    return labels


def train():
    origin_records = origin_data_reader.get_origin_records()

    # convert origin data to assembled data
    labeled_records = labeler.label_reocrd(origin_records, DAYS, THRESHOLD)

    # conduct neural network
    input = tf.placeholder(dtype=tf.float32, shape=[None, n_input])
    target = tf.placeholder(dtype=tf.float32, shape=[None, n_label])

    W1 = tf.Variable(tf.random_normal(shape=[n_input, n_label]))
    b1 = tf.Variable(tf.random_normal(shape=[n_label]))
    output1 = tf.add(tf.matmul(input, W1), b1)

    output = output1
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=target, logits=output))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(max_epoch):
            iter_size = len(labeled_records) // batch_size
            for iteration in range(iter_size):
                batch_records = labeled_records[iteration * batch_size: (iteration + 1) * batch_size]

                input_data = get_features(batch_records)
                input_data = np.reshape(input_data, [batch_size, n_input])
                target_data = get_labels(batch_records)
                target_data = np.reshape(target_data, [batch_size, n_label])

                _, data_loss = sess.run([optimizer, loss], feed_dict={input:input_data, target:target_data})
                if iteration + 1 == iter_size:
                    print("epoch #{}, loss = {}".format(epoch, data_loss))

train()