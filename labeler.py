from entity.LabeledData import LabeledData
from entity.BalanceLabeledData import BalanceLabeledData

def label_price_reocrd(records, days, threshold):
    labeled_records = []
    for i in range(days, len(records) - days + 1):
        labeled_records.append(LabeledData(records, i, days, threshold))

    return labeled_records


def get_price_feature_record(records, days, threshold):
    labeled_records = []
    for i in range(days, len(records)):
        labeled_records.append(LabeledData(records, i, days, threshold))

    return labeled_records


def label_balance_reocrd(records, days, threshold):
    labeled_records = []
    for i in range(days, len(records) - days + 1):
        labeled_records.append(BalanceLabeledData(records, i, days, threshold))

    return labeled_records


def get_balance_feature_record(records, days, threshold):
    labeled_records = []
    for i in range(days, len(records)):
        labeled_records.append(BalanceLabeledData(records, i, days, threshold))

    return labeled_records
