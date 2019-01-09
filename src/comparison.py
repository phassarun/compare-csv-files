import os

import pandas as pd
from pandas.util.testing import array_equivalent


def compare(df_current, df_past, columns):
    df_updated = pd.DataFrame(columns=columns)

    for product_code in df_current['product_code']:
        row_current = df_current.loc[df_current['product_code'] == product_code]
        row_past = df_past.loc[df_past['product_code'] == product_code]

        if not array_equivalent(row_current, row_past):
            df_updated = df_updated.append(row_current)
            print('current\t: ', row_current.values)
            print('past\t\t: ', row_past.values)
            print('#'*60)
    
    return df_updated

def create_csv_from_dataframe(df, path, suffix='updated'):
    if not os.path.exists(path):
        os.makedirs(path)

    filename = path.split('/')[-1]
    df.to_csv('{}/{}-{}.csv'.format(path, filename, suffix))
    print('Create CSV file finished!')
