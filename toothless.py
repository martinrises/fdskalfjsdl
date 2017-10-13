import random

import numpy as np
import tensorflow as tf

import labeler
import origin_data_reader
from checker.nn_market_checker import NnMarketChecker

DAYS = 26
FEATURE_SIZE = 1
THRESHOLD = 0.15
n_input = FEATURE_SIZE * DAYS
n_label = 3
n_hidden_layer = 3
n_hidden_unit = 5
learning_rate = 0.001
batch_size = 300
max_epoch = 10000


SUMMARY_DIR = './summary'
TRAIN_SUMMARY_DIR = SUMMARY_DIR+"/train"
CV_SUMMARY_DIR = SUMMARY_DIR+"/cv"
TEST_SUMMARY_DIR = SUMMARY_DIR+"/test"
CKPT_DIR = './model/{}/{}/{}/'.format(FEATURE_SIZE, n_hidden_layer, n_hidden_unit)
ACTUAL_CKPT_DIR = CKPT_DIR


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
    output = tf.nn.relu(output)
    return output


def get_random_segment(records, batch_size = batch_size):
    index = random.choice(range(len(records) - batch_size + 1))
    return records[index: index + batch_size]


def train():
    origin_records = origin_data_reader.get_b50_records()

    # convert origin data to assembled data
    labeled_records_list = labeler.get_b50_feature_record(origin_records, DAYS, THRESHOLD)
    train_records_list = []
    cv_records_list = []
    test_records_list = []
    for labeled_records in labeled_records_list:
        length = len(labeled_records)
        train_records_list.append(labeled_records[:int(0.6 * length)])
        cv_records_list.append(labeled_records[int(0.6 * length):int(0.8 * length)])
        test_records_list.append(labeled_records[int(0.8 * length):])
    train_records = [j for i in train_records_list for j in i]
    cv_records = [j for i in cv_records_list for j in i]
    test_records = [j for i in test_records_list for j in i]

    # conduct neural network
    global_step, input, output, target = get_neural_network()

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

                _ = sess.run(optimizer, feed_dict={input:input_data, target:target_data})
                if iteration % 10 == 0:
                    data_loss, train_summary = sess.run([loss, merged_summary], feed_dict={input:input_data, target:target_data})
                    train_writer.add_summary(train_summary, global_step=(global_step.eval(sess)))
                    print("epoch #{} iteration = {}, loss = {}".format((global_step.eval(sess) // iter_size), (global_step.eval(sess)), data_loss))

                    batch_cv_records = get_random_segment(cv_records)
                    cv_summary = sess.run(merged_summary, feed_dict={
                        input: np.reshape(get_features(batch_cv_records), [batch_size, n_input]),
                        target: np.reshape(get_labels(batch_cv_records), [batch_size, n_label])})
                    cv_writer.add_summary(cv_summary, global_step=(global_step.eval(sess)))

                    batch_test_records = get_random_segment(test_records)
                    test_summary = sess.run(merged_summary, feed_dict={
                        input: np.reshape(get_features(batch_test_records), [batch_size, n_input]),
                        target: np.reshape(get_labels(batch_test_records), [batch_size, n_label])})
                    test_writer.add_summary(test_summary, global_step=(global_step.eval(sess)))

            if ((global_step.eval(sess) // iter_size) + 1) % 5 == 0:
                saver.save(sess, CKPT_DIR, global_step=(global_step.eval(sess) // iter_size))


def get_neural_network():
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
    return global_step, input, output, target

def transaction():
    origin_records = origin_data_reader.get_b50_records()

    # convert origin data to assembled data
    labeled_records_list = labeler.get_b50_feature_record(origin_records, DAYS, THRESHOLD)
    train_records_list = []
    cv_records_list = []
    test_records_list = []
    for labeled_records in labeled_records_list:
        length = len(labeled_records)
        train_records_list.append(labeled_records[:int(0.6 * length)])
        cv_records_list.append(labeled_records[int(0.6 * length):int(0.8 * length)])
        test_records_list.append(labeled_records[int(0.8 * length):])
    test_records = test_records_list[3]

    _global_step, input, _output, _target = get_neural_network()
    output = tf.nn.softmax(_output)
    saver = tf.train.Saver()
    checker = NnMarketChecker(test_records)

    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state(ACTUAL_CKPT_DIR)
        saver.restore(sess, ckpt.model_checkpoint_path)

        for i in range(len(test_records) - 2):
            record = test_records[i]
            actual_input = np.reshape(get_features([record]), [1, n_input])
            output_vector = sess.run(output, feed_dict={input: actual_input})
            print("{}, {}, {}, {}, {}, {}".format(record.date, output_vector, np.argmax(output_vector), record.label, np.argmax(record.label), record.close))
            checker.on_day_triggerd(i, output_vector)

        checker.finish(len(test_records) - 2)

def predict():
    origin_records = origin_data_reader.get_origin_records()
    labeled_records = labeler.get_price_feature_record(origin_records, DAYS, THRESHOLD)

    _global_step, input, _output, _target = get_neural_network()
    output = tf.nn.softmax(_output)
    saver = tf.train.Saver()

    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state(ACTUAL_CKPT_DIR)
        saver.restore(sess, ckpt.model_checkpoint_path)

        input_records = labeled_records[-120:]
        for i in range(len(input_records)):
            record = input_records[i]
            actual_input = np.reshape(get_features([record]), [1, n_input])
            output_vector = sess.run(output, feed_dict={input: actual_input})
            print("{}, {}, {}, {}, {}, {}".format(record.date, output_vector, np.argmax(output_vector), record.label, np.argmax(record.label), record.close))


transaction()