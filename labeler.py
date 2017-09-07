from entity.LabeledData import LabeledData

def label_reocrd(records, days, threshold):
    labeled_records = []
    for i in range(days, len(records) - days + 1):
        labeled_records.append(LabeledData(records, i, days, threshold))

    return labeled_records
