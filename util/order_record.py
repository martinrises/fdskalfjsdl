import pandas as pd

with open("../data/label_result.csv", 'r') as f:
    df = pd.read_csv(f)
    values = df.iloc[:,:].values

    values = list(filter(lambda item: int(item[0].split("_")[0]) < 20, values))
    values = sorted(values, key=lambda item: item[1])

    for value in values:
        print(value)