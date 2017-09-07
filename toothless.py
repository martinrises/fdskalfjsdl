import origin_data_reader
import labeler
import tensorflow as tf
import numpy as np

DAYS = 5
FEATURE_SIZE = 4
THRESHOLD = 0.01
n_input = FEATURE_SIZE * DAYS
n_label = 3
n_hidden_layer = 3
n_hidden_unit = 5
learning_rate = 0.0001
batch_size = 30
max_epoch = 5000


SUMMARY_DIR = './summary/'


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

def layer(input, n_input, n_output):
    W = tf.Variable(tf.random_normal(shape=[n_input, n_output]))
    b = tf.Variable(tf.random_normal(shape=[n_output]))
    output = tf.add(tf.matmul(input, W), b)
    return output

def train():
    origin_records = origin_data_reader.get_origin_records()

    # convert origin data to assembled data
    labeled_records = labeler.label_reocrd(origin_records, DAYS, THRESHOLD)

    # conduct neural network
    input = tf.placeholder(dtype=tf.float32, shape=[None, n_input])
    target = tf.placeholder(dtype=tf.float32, shape=[None, n_label])

    global_step = tf.Variable(0, trainable=False)

    # first layer
    output1 = layer(input, n_input, n_hidden_unit)

    hidden_output = hidden_input = output1
    for _ in range(n_hidden_layer - 2):
        hidden_input = hidden_output = layer(hidden_input, n_hidden_unit, n_hidden_unit)

    # last layer
    output = layer(hidden_output, n_hidden_unit, n_label)

    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=target, logits=output))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss, global_step=global_step)

    with tf.name_scope("summary"):
        tf.summary.scalar("loss: days={},threshold={},hidden_layer={},hidden_unit={},lr={},max_epoch={}".format(DAYS, THRESHOLD, n_hidden_layer, n_hidden_unit, learning_rate, max_epoch), loss)
        merged_summary = tf.summary.merge_all()

    with tf.Session() as sess:
        summary_writer = tf.summary.FileWriter(SUMMARY_DIR, sess.graph)
        sess.run(tf.global_variables_initializer())

        for epoch in range(max_epoch):
            iter_size = len(labeled_records) // batch_size
            for iteration in range(iter_size):
                batch_records = labeled_records[iteration * batch_size: (iteration + 1) * batch_size]

                input_data = get_features(batch_records)
                input_data = np.reshape(input_data, [batch_size, n_input])
                target_data = get_labels(batch_records)
                target_data = np.reshape(target_data, [batch_size, n_label])

                _, data_loss, summary = sess.run([optimizer, loss, merged_summary], feed_dict={input:input_data, target:target_data})
                if iteration + 1 == iter_size:
                    summary_writer.add_summary(summary, global_step=epoch)
                    print("epoch #{}, loss = {}".format(epoch, data_loss))

train()