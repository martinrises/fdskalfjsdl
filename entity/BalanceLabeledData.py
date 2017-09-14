from entity.LabeledData import LabeledData


class BalanceLabeledData(LabeledData):
    @property
    def features(self):
        feature_records = self.records[self.index - self.days + 1: self.index + 1]
        features = []

        price_std = feature_records[-1].close
        balance_std = feature_records[-1].balance
        for r in feature_records:
            features.extend((r.close/price_std, r.balance/balance_std))
        return features