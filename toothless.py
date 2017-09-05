from market_state_checker import MarketStateChecker
import market_state_checker
import random
import os
import csv
import quanter

DAYS = 10
CENTER_NUM = 100
RANDOM_MAX = 1.02
RANDOM_MIM = 0.98
DISTANCE_THRESHOLD = 0.8
GOLD_WIN = 0.004
GOLD_WIN_RATE = 0.6
GOLD_NUM = 20
MAX_EPOCH = 100
NEED_TRAIN = True

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

class GainResult:
    def __init__(self):
        self.gain = 0
        self.win_rate = 0
        self.times = 0
        self.win_times = 0

    def calculate_gain(self):
        self.gain = self.gain / self.times
        self.win_rate = self.win_times / self.times

class KMeansRecord:
    def __init__(self, records, index, days):
        self.records = records[index - days + 1: index + 1]
        self.gain = (records[index + int(DAYS / 2)].close - records[index + 1].open)/records[index + 1].open
        features = []

        standard_price = self.records[-1].close
        for i in range(len(self.records)):
            record = self.records[i]
            features.append(record.open / standard_price)
            features.append(record.close/standard_price)
            features.append(record.high / standard_price)
            features.append(record.low / standard_price)
        self.features = features
        self.center_index = random.choice(range(CENTER_NUM))

def get_finance_balance(path):
    with open(path, "r") as f:
        lines = f.readlines()
        result = {}
        for i in range(len(lines) - 1):
            line = lines[i]
            datas = line.split(',')
            result[datas[0]] = float((datas[-1]).strip())
        return result


def balance_str(balance):
    return str(balance) if balance != None else "0"


def get_distance(features, centers):
    distances = []
    for center in centers:
        distance = map(lambda a, c: (a - c) ** 2, features, center)
        distances.append(list(distance))

    result = map(lambda vec:sum(vec) / len(vec), distances)
    return list(result)

def get_distance_from_center(features, center):
    distance = list(map(lambda a, c: (a - c) ** 2, features, center))
    return sum(distance) / len(distance)

def sort_dictionary(dic):
    result = {}
    for key in sorted(dic.keys()):
        result[key] = dic[key]
    return result


def convert_to_float_list(two_dimension_list):
    result = []
    for i in range(len(two_dimension_list)):
        result.append(list(map(lambda e:float(e), two_dimension_list[i])))
    return result


with open("./data/daily_price.csv", "r") as src_file:
    lines = src_file.readlines()

    # ,open,close,high,low,total_turnover,volume
    keys = lines[0].strip().split(',')

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

    split_index_1 = int(len(records) * 0.6)
    split_index_2 = int(len(records) * 0.9)
    train_records = records[:split_index_1]
    cv_records = records[split_index_1: split_index_2]
    test_records = records[split_index_2:]

    centers_file_name = "./data/k_means/centers_{}_{}_{}.csv".format(str(DAYS), str(GOLD_WIN * 1000), str(GOLD_NUM))
    distances_file_name = "./data/k_means/distance_{}_{}_{}.csv".format(str(DAYS), str(GOLD_WIN * 1000), str(GOLD_NUM))
    win_rate_file_name = "./data/k_means/win_rate_{}_{}_{}.csv".format(str(DAYS), str(GOLD_WIN * 1000), str(GOLD_NUM))
    if NEED_TRAIN:
        gold_centers = []
        gold_distances = []
        gold_win_rates = []
        for train_step in range(MAX_EPOCH):
            # train
            k_means_records = []
            for i in range(DAYS, len(train_records) - DAYS):
                k_means_records.append(KMeansRecord(train_records, index=i, days=DAYS))

            centers = []
            feature_num = len(k_means_records[0].features)
            for _ in range(CENTER_NUM):
                points = []
                for __ in range(feature_num):
                    points.append(random.uniform(RANDOM_MIM, RANDOM_MAX))
                centers.append(points)

            assert(len(centers) == CENTER_NUM and len(centers[0]) == feature_num and feature_num > 0)


            while True:
                # calculate distance
                for k_means_record in k_means_records:
                    distances = get_distance(k_means_record.features, centers)
                    k_means_record.center_index = distances.index(min(distances))

                # update centers
                center_cnt = {}
                center_vecs = []
                for _ in range(len(centers)):
                    center_vecs.append([0] * feature_num)

                for k_means_record in k_means_records:
                    center_vecs[k_means_record.center_index] = list(map(lambda a,b: a+b, center_vecs[k_means_record.center_index], k_means_record.features))
                    cnt = center_cnt.get(k_means_record.center_index) if center_cnt.get(k_means_record.center_index) != None else 0
                    cnt+=1
                    center_cnt[k_means_record.center_index] = cnt

                temp_centers = []
                for i in range(len(centers)):
                    if center_cnt.get(i) != None:
                        temp_centers.append(list(map(lambda sum: sum / center_cnt.get(i), center_vecs[i])))

                # check whether centers changed
                if temp_centers == centers:
                    break;
                else:
                    centers = temp_centers

            center_cnt = {}
            distribute_distances = {}
            for k_means_record in k_means_records:
                index = k_means_record.center_index
                distance = get_distance_from_center(k_means_record.features, centers[index])
                distribute_dis = distribute_distances.get(index) if distribute_distances.get(index) is not None else 0
                distribute_distances[index] = distribute_dis + distance

                cnt = center_cnt.get(index) if center_cnt.get(index) is not None else 0
                cnt += 1
                center_cnt[index] = cnt

            average_distances = {}
            distances_keys = distribute_distances.keys()
            for key in distances_keys:
                average_distances[key] = distribute_distances.get(key) / center_cnt.get(key)

            gains = {}
            for k_means_record in k_means_records:
                index = k_means_record.center_index
                distance = get_distance_from_center(k_means_record.features, centers[index])

                if distance < average_distances.get(index) * DISTANCE_THRESHOLD:
                    gain_result = gains.get(index) if gains.get(index) is not None else GainResult()
                    gain_result.times += 1
                    if k_means_record.gain > 0:
                        gain_result.win_times += 1

                    gain_result.gain += k_means_record.gain
                    gains[index] = gain_result

            for key in gains.keys():
                gain_record = gains.get(key)
                gain_record.calculate_gain()

            result_dic = sort_dictionary(gains)
            print("centers.size = {}".format(len(centers)))
            print("centers = {}".format(centers))
            print("center_cnt = {}".format(sort_dictionary(center_cnt)))
            print("center_real_cnt = {}".format({key: value.times for key, value in result_dic.items()}))
            print("win_rate = {}".format({key: value.win_rate for key, value in result_dic.items()}))
            print("gains = {}".format({key: value.gain for key, value in result_dic.items()}))

            # cross validation
            k_means_cv_records = []
            for i in range(DAYS, len(cv_records) - DAYS):
                k_means_cv_records.append(KMeansRecord(cv_records, index=i, days=DAYS))

            cv_gains = {}
            cv_center_cnt = {}
            for k_means_record in k_means_cv_records:
                distances = get_distance(k_means_record.features, centers)
                k_means_record.center_index = distances.index(min(distances))

                index = k_means_record.center_index
                distance = distances[index]

                cnt = cv_center_cnt.get(index) if cv_center_cnt.get(index) is not None else 0
                cnt += 1
                cv_center_cnt[index] = cnt

                if distance < average_distances.get(index) * DISTANCE_THRESHOLD:
                    gain_result = cv_gains.get(index) if cv_gains.get(index) is not None else GainResult()
                    gain_result.times += 1

                    if k_means_record.gain > 0:
                        gain_result.win_times += 1

                    gain_result.gain += k_means_record.gain
                    cv_gains[index] = gain_result

            for key in cv_gains.keys():
                gain = cv_gains.get(key)
                gain.calculate_gain()

            result_dic = sort_dictionary(cv_gains)
            print("\ncross validation\ncenters = {}".format(centers))
            print("center_cnt = {}".format(sort_dictionary(cv_center_cnt)))
            print("center_real_cnt = {}".format({key: value.times for key, value in result_dic.items()}))
            print("center_win_rate = {}".format({key: value.win_rate for key, value in result_dic.items()}))
            print("gains = {}".format({key: value.gain for key, value in result_dic.items()}))

            # gold centers
            for i in range(len(centers)):
                center = centers[i]
                if center in gold_centers:
                    continue

                gain_result = gains.get(i)
                cv_gain_result = cv_gains.get(i)
                if gain_result is not None and cv_gain_result is not None\
                        and gain_result.gain > GOLD_WIN \
                        and cv_gain_result.gain > GOLD_WIN \
                        and gain_result.times > GOLD_NUM \
                        and cv_gain_result.times > GOLD_NUM\
                        and gain_result.win_rate > GOLD_WIN_RATE\
                        and cv_gain_result.win_rate > GOLD_WIN_RATE:
                    gold_centers.append(center)
                    gold_distances.append(average_distances.get(i))
                    gold_win_rates.append((gains.get(i).win_rate + cv_gains.get(i).win_rate) / 2)

            print("\n step # {}, gold_centers.size = {}\n\n".format(train_step, len(gold_centers)))


        print("\ngold_centers.size = {}".format(len(gold_centers)))

        is_file_exist = os.path.isfile(centers_file_name)
        center_in_file = []
        if is_file_exist:
            with open(centers_file_name, "r") as centers_f:
                center_f_csv_reader = csv.reader(centers_f)
                center_in_file = list(center_f_csv_reader)

        open_mode = "a" if is_file_exist else "w"
        with open(centers_file_name, open_mode, newline='') as centers_f,\
                open(distances_file_name, open_mode, newline='') as distances_f, \
                open(win_rate_file_name, open_mode, newline='') as win_rate_f:

            center_f_csv_writer = csv.writer(centers_f)
            distance_f_csv_writer = csv.writer(distances_f)
            win_rate_f_csv_writer = csv.writer(win_rate_f)

            for i in range(len(gold_centers)):
                center = gold_centers[i]
                distance = gold_distances[i]
                win_rate = gold_win_rates[i]

                if center not in center_in_file:
                    center_f_csv_writer.writerow(center)
                    distances_f.write(str(distance) + "\n")
                    win_rate_f.write(str(win_rate) + "\n")

    # test
    # get gold_centers and gold_distances from file
    gold_centers = None
    gold_distances = None
    with open(centers_file_name, 'r') as centers_f , open(distances_file_name, 'r') as distances_f:
        center_csv_reader = csv.reader(centers_f)
        gold_centers = list(center_csv_reader)

        gold_centers = convert_to_float_list(gold_centers)

        distances_csv_reader = csv.reader(distances_f)
        gold_distances = list(distances_csv_reader)
        gold_distances = convert_to_float_list(gold_distances)

    k_means_test_records = []
    for i in range(DAYS, len(test_records) - DAYS):
        k_means_test_records.append(KMeansRecord(test_records, index=i, days=DAYS))

    test_gains = {}
    test_center_cnt = {}
    for k_means_record in k_means_test_records:
        distances = get_distance(k_means_record.features, gold_centers)
        for i in range(len(gold_centers)):
            distance = distances[i]
            if distance <= gold_distances[i][0] * DISTANCE_THRESHOLD:
                gain_result = test_gains.get(i) if test_gains.get(i) is not None else GainResult()
                gain_result.gain += k_means_record.gain
                gain_result.times += 1
                if k_means_record.gain > 0:
                    gain_result.win_times += 1
                test_gains[i] = gain_result


    for key in test_gains.keys():
        gain_record = test_gains.get(key)
        gain_record.calculate_gain()

    gain_records = sort_dictionary(test_gains)
    print("\ntest\ncenters = {}".format(gold_centers))
    print("center_real_cnt = {}".format({key: value.times for key, value in test_gains.items()}))
    print("win_rate = {}".format({key: value.win_rate for key, value in test_gains.items()}))
    print("gains = {}".format({key: value.gain for key, value in test_gains.items()}))