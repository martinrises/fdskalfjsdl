import math

class LabeledData:
    def __init__(self, records, index, days, threshold):
        self.records = records
        self.index = index
        self.days = days
        self.threshold = threshold


    @property
    def label(self):
        if self.index + int(self.days/ 2) >= len(self.records):
            return [0, 0, 0]

        high = max([r.high for r in self.records][self.index - self.days: self.index + 1])
        low = min([r.low for r in self.records][self.index - self.days: self.index + 1])
        curr_record = self.records[self.index]
        future_record = self.records[self.index + int(self.days/3)]
        delta_threshold = (high - low) * self.threshold
        delta = future_record.close - curr_record.close
        if delta > 0 and delta > delta_threshold:
            return 0
        elif delta < 0 and -delta > delta_threshold:
            return 1
        else:
            return 2

    @property
    def features(self):
        feature_records = self.records[self.index - self.days + 1: self.index + 1]
        features = []

        price_std = feature_records[-1].open
        for r in feature_records:
            features.extend([r.close/price_std])
        return features

    @property
    def date(self):
        return self.records[self.index].date

    @property
    def open(self):
        return self.records[self.index].open

    @property
    def close(self):
        return self.records[self.index].close

    @property
    def year(self):
        return self.records[self.index].date.split('-')[0]