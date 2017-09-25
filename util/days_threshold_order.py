import origin_data_reader
import labeler
import csv
import time


def get_order():
    origin_records = origin_data_reader.get_b50_records(path='../data/b50/')

    f = open("../data/pick_days_threshold.csv", 'a', newline='')
    csv_writer = csv.writer(f)

    for days in range(14, 51):
        for i in range(1, 7):
            change_cnt = 0
            up_cnt = shake_cnt = down_cnt = 0
            threshold = i*0.05
            records = labeler.get_b50_feature_record(origin_records, days, threshold)
            records = [j for i in records for j in i]

            label = records[0].label
            if label == 0:
                up_cnt += 1
            elif label == 1:
                shake_cnt += 1
            else:
                down_cnt += 1
            print(len(records))
            start_ts = time.process_time()
            for index in range(1, len(records)):
                print(index)
                last_r = records[index - 1]
                curr_r = records[index]

                last_label = last_r.label
                curr_label = curr_r.label

                if last_label != curr_label:
                    change_cnt += 1

                label = curr_label
                if label == 0:
                    up_cnt += 1
                elif label == 1:
                    shake_cnt += 1
                else:
                    down_cnt += 1
            data = [up_cnt, down_cnt, shake_cnt]
            print(data)
            temp = [days, str(threshold), change_cnt * sum(data) / min(data)]
            temp.extend(data)
            csv_writer.writerow(temp)
            print("time = {}".format(time.process_time() - start_ts))
            print(temp)

    f.close()

def show_order():
    f = open("../data/pick_days_threshold.csv", 'r', newline='')
    b50_result = csv.reader(f)
    result = sorted(b50_result, key=lambda item:item[2])
    for item in result:
        print(item)

show_order()

