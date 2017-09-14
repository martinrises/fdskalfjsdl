import pandas as pd
from entity.OriginRecord import OriginRecord
from entity.BalanceRecord import BalanceRecord
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


def get_balance_records(price_path='./data/daily_price.csv', balance_path='./data/balance_origin.txt'):

    balance_f = open(balance_path, 'r')
    price_records = get_origin_records(price_path)
    price_records = {r.date:r for r in price_records}

    balance_df = pd.read_csv(balance_f)
    balance_values = balance_df.iloc[:,:].values
    balance_records = []
    for i in range(len(balance_values)):
        value = balance_values[i]
        price_record = price_records[value[0]]
        balance = value[-1]
        balance_records.append(BalanceRecord(price_record.date,
                                             price_record.open,
                                             price_record.close,
                                             price_record.high,
                                             price_record.low,
                                             price_record.volume,
                                             price_record.turnover,
                                             balance))
    balance_f.close()
    return sorted(balance_records, key=lambda r: r.date)
