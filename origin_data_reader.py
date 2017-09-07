import pandas as pd
from entity.OriginRecord import OriginRecord
import numpy as np

def read_origin_data(path='./data/daily_price.csv'):
    '''
    read origin data
    :param path:
    :param n_inputs:
    :return:
    '''
    f = open(path)
    df = pd.read_csv(f)
    data = df.iloc[:, :].values
    f.close()
    return data

def get_origin_records(path='./data/daily_price.csv'):
    f = open(path)
    df = pd.read_csv(f)
    len = df.shape[0]
    records = []
    for i in range(len):
        records.append(OriginRecord(df.iloc[i,0],
                                    df.open[i],
                                    df.close[i],
                                    df.high[i],
                                    df.low[i],
                                    df.volume[i],
                                    df.total_turnover[i]))
    f.close()
    # 2005-01-04,1260.782,1242.774,1260.782,1238.179,4418452047.0,816177000.0
    first_record = records[0]
    assert first_record.date == '2005-01-04'
    assert str(first_record.open) == '1260.782'
    assert str(first_record.close) == '1242.774'
    assert str(first_record.high) == '1260.782'
    assert str(first_record.low) == '1238.179'
    assert str(first_record.volume) == '816177000.0'
    assert str(first_record.turnover) == '4418452047.0'

    return records