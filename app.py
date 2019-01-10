import os
from enum import Enum

import pandas as pd

from src.computation import compare, report
from src.snippets import (download_blob, filter_by_country_code,
                          get_prefix_list, is_lang, list_blobs_with_prefix)


class Lang(Enum):
    EN = 'EN'
    TH = 'TH'


if __name__ == "__main__":
    export_folder = 'export'
    update_folder = 'updated'
    report_file_name = 'stores-report.csv'
    bucket_name = 'pricetrolley-prod_scraper'

    compare_columns = ['product_code', 'regular_price', 'discount']
    report_columns = ['store_name', 'diff (%)', 'updated', 'original']
    df_summary_report = pd.DataFrame(columns=report_columns)

    if not os.path.exists(export_folder):
        os.mkdir(export_folder)

    prefix_list = get_prefix_list(bucket_name)
    for prefix in prefix_list:
        # get list files
        list_blobs = list_blobs_with_prefix(bucket_name, prefix)

        lang_en = is_lang(list_blobs, Lang.EN.value)
        if lang_en:
            filtered_list_blobs = filter_by_country_code(list_blobs, Lang.EN.value)
        else:
            filtered_list_blobs = filter_by_country_code(list_blobs, Lang.TH.value)
        
        # download file
        destination_file_name_current = '{}/{}'.format(export_folder, filtered_list_blobs[-1])
        destination_file_name_current
        download_blob(bucket_name, filtered_list_blobs[-1], destination_file_name_current)

        destination_file_name_past = '{}/{}'.format(export_folder, filtered_list_blobs[-2])
        download_blob(bucket_name, filtered_list_blobs[-2], destination_file_name_past)

        # create DataFrame from csv
        df_current = pd.read_csv(destination_file_name_current)[compare_columns].drop_duplicates(subset='product_code')
        df_past = pd.read_csv(destination_file_name_past)[compare_columns].drop_duplicates(subset='product_code')
        # generate DataFrame has changed
        df_updated = compare(df_current, df_past, compare_columns)

        # create update csv
        dir_updated = '{}/{}'.format(update_folder, prefix)
        if not os.path.exists(dir_updated):
            os.makedirs(dir_updated)
        destination_file_name_updated = '{}/{}-{}.csv'.format(dir_updated, prefix, update_folder)
        df_updated.to_csv(destination_file_name_updated)

        # generate report
        df_report = report(df_updated, df_current, store_name=prefix)
        df_summary_report = df_summary_report.append(df_report)

    # create report csv
    df_summary_report.to_csv(report_file_name)
