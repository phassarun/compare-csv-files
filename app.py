import os

import pandas as pd

from src.comparison import compare, create_csv_from_dataframe
from src.csv_files_downloader import download_csv_files, get_prefix_list


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

if __name__ == "__main__":
    export_folder = 'export'
    update_folder = 'updated'
    bucket_name = 'pricetrolley-prod_scraper'
    list_index = [-1, -2] # -1 is current file, -2 is past file

    report_columns = ['store_name', 'diff (%)', 'updated', 'original']
    df_summary_report = pd.DataFrame(columns=report_columns)

    compare_columns = ['product_code', 'regular_price', 'discount']
    prefix_list = get_prefix_list(bucket_name)
    for prefix in prefix_list:
        path_csv_files = download_csv_files(bucket_name, prefix, list_index, export_folder)
        # path_csv_files 0 is latest, 1 is (latest-1)
        df_current = pd.read_csv(path_csv_files[0])[compare_columns].drop_duplicates(subset='product_code')
        df_past = pd.read_csv(path_csv_files[1])[compare_columns].drop_duplicates(subset='product_code')
        df_updated = compare(df_current, df_past, compare_columns)
        
        # create updated csv
        path_output_csv = '{}/{}'.format(update_folder, prefix)
        create_csv_from_dataframe(df_updated, path_output_csv, suffix='updated')

        # create report csv
        print(path_csv_files[0])
        df_report = report(df_updated, df_current, store_name=prefix)
        df_summary_report = df_summary_report.append(df_report)

    df_summary_report.to_csv('stores-report.csv')
