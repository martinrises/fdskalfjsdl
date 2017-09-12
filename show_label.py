import origin_data_reader
import labeler
import matplotlib.pyplot as plt
import numpy as np
import csv

result = {}
day = 12
threshold = 0.2


origin_records = origin_data_reader.get_origin_records()
records = labeler.label_reocrd(origin_records, day, threshold)

plt.plot(range(len(records)), [r.label for r in records])
plt.show()