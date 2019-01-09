import os

import pandas as pd

from src.comparison import compare_csv_files, create_csv_from_dataframe
from src.csv_files_downloader import download_csv_files, get_prefix_list


def report(df_1, df_2, store_name):
    columns = ['product_code']
    df_1_count = df_1.count()[columns]
    df_2_count = df_2.count()[columns]
    
    report_columns = ['store_name', 'diff (%)', 'updated', 'original']
    df_report = pd.DataFrame(columns=report_columns)
    df_report['diff (%)'] = df_2_count/df_1_count*100
    df_report['updated'] = df_2_count
    df_report['original'] = df_1_count
    df_report['store_name'] = store_name

    print(df_report)
    print('#'*60)

    return df_report

if __name__ == "__main__":
    export_folder = 'export'
    update_folder = 'updated'
    bucket_name = 'pricetrolley-prod_scraper'

    columns = ['store_name', 'diff (%)', 'updated', 'original']
    df_output = pd.DataFrame(columns=columns)

    prefix_list = get_prefix_list(bucket_name)
    for prefix in prefix_list:
        list_index = [-1, -2] # -1 is current file, -2 is past file

        path_csv_files = download_csv_files(bucket_name, prefix, list_index, export_folder)
        df_updated = compare_csv_files(path_csv_files[0], path_csv_files[1])
        
        # create updated csv
        path_output_csv = '{}/{}'.format(update_folder, prefix)
        create_csv_from_dataframe(df_updated, path_output_csv, suffix='updated')

        # create report csv
        print(path_csv_files[0])
        df_original = pd.read_csv(path_csv_files[0])
        df_report = report(df_original, df_updated, store_name=prefix)
        df_output = pd.concat([df_output, df_report])

    df_output.to_csv('stores-report.csv')
