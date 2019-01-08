import os
import pandas as pd
from pandas.util.testing import array_equivalent

def compare_csv_files(file_1, file_2, dir_folder):
    file_1 = '{}/{}'.format(dir_folder, file_1)
    file_2 = '{}/{}'.format(dir_folder, file_2)
    df_current = pd.read_csv(file_1)
    df_past = pd.read_csv(file_2)

    columns = ['product_code', 'name', 'regular_price', 'discount']
    df_current = df_current[columns]
    df_past = df_past[columns]

    df_updated = pd.DataFrame(columns=columns)

    for product_code in df_current['product_code']:
        row_current = df_current.loc[df_current['product_code'] == product_code]
        row_past = df_past.loc[df_past['product_code'] == product_code]

        if not array_equivalent(row_current, row_past):
            print('current\t: ', row_current.values)
            print('past\t\t: ', row_past.values)
            df_updated = pd.concat([df_updated, row_current])
            print('#'*60)
    
    df_updated.to_csv('demo.csv')


if __name__ == "__main__":
    dir_folder = 'export/redmart'
    list_csv_files = os.listdir(dir_folder)
    compare_csv_files(list_csv_files[-2], list_csv_files[-1], dir_folder)



