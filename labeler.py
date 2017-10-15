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

def get_b50_feature_record(records, days, threshold):
    labeled_records_result = []
    for record_list in records:
        labeled_records = []
        for i in range(days, len(record_list)):
            labeled_records.append(LabeledData(record_list, i, days, threshold))
        labeled_records_result.append(labeled_records)
    return labeled_records_result

def get_future_feature_record(records, days, threshold):
    labeled_records_result = []
    for _, record_list in records.items():
        labeled_records = []
        for i in range(days, int(len(record_list) - days/2)):
            labeled_records.append(LabeledData(record_list, i, days, threshold))
        labeled_records_result.append(labeled_records)
    return labeled_records_result