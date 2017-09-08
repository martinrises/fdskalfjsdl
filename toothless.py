import origin_data_reader
import labeler
import tensorflow as tf
import numpy as np
import random

DAYS = 5
FEATURE_SIZE = 4
THRESHOLD = 0.01
n_input = FEATURE_SIZE * DAYS
n_label = 3
n_hidden_layer = 3
n_hidden_unit = 5
learning_rate = 0.001
batch_size = 30
max_epoch = 10000


SUMMARY_DIR = './summary'
TRAIN_SUMMARY_DIR = SUMMARY_DIR+"/train"
CV_SUMMARY_DIR = SUMMARY_DIR+"/cv"
TEST_SUMMARY_DIR = SUMMARY_DIR+"/test"
CKPT_DIR = './model/{}/{}/{}/{}'.format(FEATURE_SIZE, n_hidden_layer, n_hidden_unit, learning_rate)


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


def get_random_segment(records, batch_size = batch_size):
    index = random.choice(range(len(records) - batch_size + 1))
    return records[index: index + batch_size]


def train():
    origin_records = origin_data_reader.get_origin_records()

    # convert origin data to assembled data
    labeled_records = labeler.label_reocrd(origin_records, DAYS, THRESHOLD)
    length = len(labeled_records)
    train_records = labeled_records[:int(0.6 * length)]
    cv_records = labeled_records[len(train_records):int(0.8 * length)]
    test_records = labeled_records[len(cv_records):]

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
        tf.summary.scalar("train_loss", loss)
        merged_summary = tf.summary.merge_all()

    saver = tf.train.Saver()

    with tf.Session() as sess:
        train_writer = tf.summary.FileWriter(TRAIN_SUMMARY_DIR, sess.graph)
        cv_writer = tf.summary.FileWriter(CV_SUMMARY_DIR, sess.graph)
        test_writer = tf.summary.FileWriter(TEST_SUMMARY_DIR, sess.graph)


        ckpt = tf.train.get_checkpoint_state(CKPT_DIR)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            sess.run(tf.global_variables_initializer())

        for epoch in range(max_epoch):
            iter_size = len(train_records) // batch_size
            for iteration in range(iter_size):
                batch_records = train_records[iteration * batch_size: (iteration + 1) * batch_size]

                input_data = np.reshape(get_features(batch_records), [batch_size, n_input])
                target_data = np.reshape(get_labels(batch_records), [batch_size, n_label])

                _, data_loss, train_summary = sess.run([optimizer, loss, merged_summary], feed_dict={input:input_data, target:target_data})
                if iteration + 1 == iter_size:
                    train_writer.add_summary(train_summary, global_step=epoch)
                    print("epoch #{}, loss = {}".format(epoch, data_loss))
                    batch_cv_records = get_random_segment(cv_records)
                    cv_summary = sess.run(merged_summary, feed_dict={input: np.reshape(get_features(batch_cv_records), [batch_size, n_input]), target: np.reshape(get_labels(batch_cv_records), [batch_size, n_label])})
                    cv_writer.add_summary(cv_summary, global_step=epoch)

                    batch_test_records = get_random_segment(test_records)
                    test_summary = sess.run(merged_summary, feed_dict={input: np.reshape(get_features(batch_test_records), [batch_size, n_input]), target: np.reshape(get_labels(batch_test_records), [batch_size, n_label])})
                    test_writer.add_summary(test_summary, global_step=epoch)


            if (epoch + 1) % 1000 == 0:
                saver.save(sess, CKPT_DIR, global_step=epoch)

train()