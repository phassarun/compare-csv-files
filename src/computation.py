import os

import pandas as pd
from pandas.util.testing import array_equivalent


def compare(df_current, df_past, columns):
    df_updated = pd.DataFrame(columns=columns)
    df_diff = df_current.copy()
    df_diff['updated'] = False

    drop_columns = [
        'store_id',
        'store_name',
        'store_slug',
        'store_website',
        'scrapedAt',
        'url',
        'image',
        'category',
        'brand',
        'lang',
        'sku',
        'availability',
        'package_size',
        'halal',
        'promotion_quantity',
        'promotion_price',
        'description',
    ]

    for product_code in df_current['product_code']:
        row_current = df_current.loc[df_current['product_code'] == product_code]
        row_past = df_past.loc[df_past['product_code'] == product_code]

        if not array_equivalent(row_current.drop(columns=drop_columns), row_past.drop(columns=drop_columns)):
            df_updated = df_updated.append(row_current)
            print('current\t: ', row_current.values)
            print('past\t\t: ', row_past.values)
            index = df_diff.index[df_diff['product_code'] == product_code]
            df_diff['updated'][index] = True
            print(df_diff.loc[df_diff['product_code'] == product_code])
            print('#'*60)

    return df_updated, df_diff

def report(df_updated, df_current, store_name):
    selected_columns = ['product_code']
    df_updated = df_updated.count()[selected_columns]
    df_current = df_current.count()[selected_columns]
    
    report_columns = ['store_name', 'diff (%)', 'date', 'updated', 'original']
    df_report = pd.DataFrame(columns=report_columns)
    df_report['diff (%)'] = df_updated / df_current * 100
    df_report['updated'] = df_updated
    df_report['original'] = df_current
    df_report['store_name'] = store_name

    print(df_report)
    print('#'*60)

    return df_report
