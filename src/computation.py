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

def report(df_updated, df_current, store_name):
    selected_columns = ['product_code']
    df_updated = df_updated.count()[selected_columns]
    df_current = df_current.count()[selected_columns]
    
    report_columns = ['store_name', 'diff (%)', 'updated', 'original']
    df_report = pd.DataFrame(columns=report_columns)
    df_report['diff (%)'] = df_updated / df_current * 100
    df_report['updated'] = df_updated
    df_report['original'] = df_current
    df_report['store_name'] = store_name

    print(df_report)
    print('#'*60)

    return df_report

