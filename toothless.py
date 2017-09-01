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
DISTANCE_THRESHOLD = 0.05
GOLD_WIN = 0.005
GOLD_NUM = 25
MAX_EPOCH = 10
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

    centers_file_name = "./data/k_means/centers_" + str(DAYS) + ".csv"
    distances_file_name = "./data/k_means/distance_" + str(DAYS) + ".csv"
    if NEED_TRAIN:
        gold_centers = []
        gold_distances = []
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
                distribute_dis = distribute_distances.get(index) if distribute_distances.get(index) != None else 0
                distribute_distances[index] = distribute_dis + distance

                cnt = center_cnt.get(index) if center_cnt.get(index) != None else 0
                cnt += 1
                center_cnt[index] = cnt

            average_distance = {}
            distances_keys = distribute_distances.keys()
            for key in distances_keys:
                average_distance[key] = distribute_distances.get(key) / center_cnt.get(key)

            center_real_cnt = {}
            gains = {}
            for k_means_record in k_means_records:
                index = k_means_record.center_index
                distance = get_distance_from_center(k_means_record.features, centers[index])

                if distance < distribute_distances.get(index) * DISTANCE_THRESHOLD:
                    cnt = center_real_cnt.get(index) if center_real_cnt.get(index) != None else 0
                    cnt += 1
                    center_real_cnt[index] = cnt

                    gain = gains.get(index) if gains.get(index) != None else 0
                    gains[index] = gain + k_means_record.gain

            for key in gains.keys():
                gain = gains.get(key)
                real_cnt = center_real_cnt.get(key)
                gains[key] = gain/real_cnt

            print("centers.size = {}".format(len(centers)))
            print("centers = {}".format(centers))
            print("center_cnt = {}".format(sort_dictionary(center_cnt)))
            print("cneter_real_cnt = {}".format(sort_dictionary(center_real_cnt)))
            print("gains = {}".format(sort_dictionary(gains)))

            # cross validation
            k_means_cv_records = []
            for i in range(DAYS, len(cv_records) - DAYS):
                k_means_cv_records.append(KMeansRecord(cv_records, index=i, days=DAYS))

            cv_center_real_cnt = {}
            cv_gains = {}
            cv_center_cnt = {}
            for k_means_record in k_means_cv_records:
                distances = get_distance(k_means_record.features, centers)
                k_means_record.center_index = distances.index(min(distances))

                index = k_means_record.center_index
                distance = distances[index]

                cnt = cv_center_cnt.get(index) if cv_center_cnt.get(index) != None else 0
                cnt += 1
                cv_center_cnt[index] = cnt

                if distance < distribute_distances.get(index) * DISTANCE_THRESHOLD:
                    cnt = cv_center_real_cnt.get(index) if cv_center_real_cnt.get(index) != None else 0
                    cnt += 1
                    cv_center_real_cnt[index] = cnt

                    gain = cv_gains.get(index) if cv_gains.get(index) != None else 0
                    cv_gains[index] = gain + k_means_record.gain

            for key in cv_gains.keys():
                gain = cv_gains.get(key)
                real_cnt = cv_center_real_cnt.get(key)
                cv_gains[key] = gain / real_cnt

            print("\ncenters = {}".format(centers))
            print("center_cnt = {}".format(sort_dictionary(cv_center_cnt)))
            print("cneter_real_cnt = {}".format(sort_dictionary(cv_center_real_cnt)))
            print("gains = {}".format(sort_dictionary(cv_gains)))

            # gold centers
            for i in range(len(centers)):
                center = centers[i]
                if center in gold_centers:
                    continue

                if gains.get(i) != None and gains.get(i) > GOLD_WIN and cv_gains.get(i) != None and cv_gains.get(i) > GOLD_WIN and center_real_cnt.get(i) and center_real_cnt.get(i) != None and center_real_cnt.get(i) > GOLD_NUM and cv_center_real_cnt.get(i) != None and cv_center_real_cnt.get(i) > GOLD_NUM:
                    gold_centers.append(center)
                    gold_distances.append(distribute_distances.get(i))

            print("\n step # {}, gold_centers.size = {}\n\n".format(train_step, len(gold_centers)))


        print("\ngold_centers.size = {}".format(len(gold_centers)))

        is_file_exist = os.path.isfile(centers_file_name)
        open_mode = "a" if is_file_exist else "w"
        with open(centers_file_name, open_mode, newline='') as centers_f, open(distances_file_name, open_mode) as distances_f:
            center_f_csv_writer = csv.writer(centers_f)
            for center in gold_centers:
                center_f_csv_writer.writerow(center)
            for distance in gold_distances:
                distances_f.write(str(distance) + "\n")

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

    test_center_real_cnt = {}
    test_gains = {}
    test_center_cnt = {}
    for k_means_record in k_means_test_records:
        distances = get_distance(k_means_record.features, gold_centers)
        for i in range(len(gold_centers)):
            distance = distances[i]
            if distance <= gold_distances[i][0] * DISTANCE_THRESHOLD:
                cnt = test_center_real_cnt.get(i) if test_center_real_cnt.get(i) != None else 0
                cnt += 1
                test_center_real_cnt[i] = cnt

                gain = test_gains.get(i) if test_gains.get(i) != None else 0
                test_gains[i] = gain + k_means_record.gain


    for key in test_gains.keys():
        gain = test_gains.get(key)
        real_cnt = test_center_real_cnt.get(key)
        test_gains[key] = gain / real_cnt

    print("\ncenters = {}".format(gold_centers))
    print("cneter_real_cnt = {}".format(sort_dictionary(test_center_real_cnt)))
    print("gains = {}".format(sort_dictionary(test_gains)))