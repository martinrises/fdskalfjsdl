import math

class LabeledData:
    def __init__(self, records, index, days, threshold):
        self.records = records
        self.index = index
        self.days = days
        self.threshold = threshold


    @property
    def label(self):
        high = max([r.high for r in self.records][self.index - self.days: self.index + 1])
        low = min([r.low for r in self.records][self.index - self.days: self.index + 1])
        curr_record = self.records[self.index]
        future_record = self.records[self.index + int(self.days/ 2)]
        delta_threshold = (high - low) * self.threshold
        delta = future_record.close - curr_record.close
        if delta > 0 and delta > delta_threshold:
            return [1, 0, 0]
        elif delta < 0 and -delta > delta_threshold:
            return [0, 0, 1]
        else:
            return [0, 1, 0]

    @property
    def features(self):
        feature_records = self.records[self.index - self.days + 1: self.index + 1]
        features = []

        price_std = feature_records[-1].open
        volume_std = feature_records[-1].volume
        turnover_std = feature_records[-1].turnover
        for r in feature_records:
            # features.extend((r.open/price_std, r.close/price_std, r.high/price_std, r.low/price_std, r.volume/volume_std, r.turnover/turnover_std))
            features.extend((r.open/price_std, r.close/price_std, r.high/price_std, r.low/price_std))
        return features

    @property
    def date(self):
        return self.records[self.index].date