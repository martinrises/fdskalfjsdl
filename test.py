import origin_data_reader
import labeler
import matplotlib.pyplot as plt
import numpy as np

result = {}


def get_change_counts(records):
    internal_cnt = 0
    up_cnt = 0
    shake_cnt = 0
    down_cnt = 0
    for i in range(1, len(records)):
        if records[i].label != records[i - 1].label:
            internal_cnt += 1

        if records[i].label == 2:
            up_cnt += 1
        elif records[i].label == 1:
            shake_cnt += 1
        else:
            down_cnt += 1
    return internal_cnt, up_cnt, shake_cnt, down_cnt


for day  in range(2, 61):
    for threshold in np.linspace(start=0.05, stop=1.05, num=20):
        origin_records = origin_data_reader.get_origin_records()
        records = labeler.label_reocrd(origin_records, day, threshold)
        cnt, up_cnt, shake_cnt, down_cnt = get_change_counts(records)
        print("{}_{} >>> {}".format(day, threshold, cnt / min([up_cnt, shake_cnt, down_cnt]) * sum([up_cnt, shake_cnt, down_cnt])))
        result["{}_{}".format(day, threshold)] = cnt / min([up_cnt, shake_cnt, down_cnt]) * sum([up_cnt, shake_cnt, down_cnt])

result = {item[0]: item[1] for item in sorted(result.items(), key=lambda item: item[1])}
print(result)
