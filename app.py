import os
from enum import Enum

import pandas as pd

from src.computation import compare, report
from src.snippets import (download_blob, filter_by_country_code,
                          filter_by_month_year, get_prefix_list, is_lang,
                          list_blobs_with_prefix)


class Lang(Enum):
    EN = 'EN'
    TH = 'TH'


if __name__ == "__main__":
    export_folder = 'export'
    update_folder = 'updated'
    report_file_name = 'stores-report.csv'
    bucket_name = 'pricetrolley-prod_scraper'

    compare_columns = [
        'store_id',
        'store_name',
        'store_slug',
        'store_website',
        'scrapedAt',
        'product_code',
        'name',
        'url',
        'image',
        'regular_price',
        'discount',
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

    month_year = '2018-12'

    report_columns = ['store_name', 'diff (%)', 'updated', 'original']
    df_summary_report = pd.DataFrame(columns=report_columns)

    

    if not os.path.exists(export_folder):
        os.mkdir(export_folder)

    # prefix_list = get_prefix_list(bucket_name)
    prefix_list = ['tops', 'cp-freshmart', 'makro', 'tesco-lotus', 'big-c']
    # prefix_list = ['redmart']
    for prefix in prefix_list:
        # get list files
        list_blobs = list_blobs_with_prefix(bucket_name, prefix)
        list_blobs = filter_by_month_year(list_blobs, month_year)

        lang_en = is_lang(list_blobs, Lang.EN.value)
        if lang_en:
            filtered_list_blobs = filter_by_country_code(list_blobs, Lang.EN.value)
        else:
            filtered_list_blobs = filter_by_country_code(list_blobs, Lang.TH.value)
        
        # download file
        for blob in filtered_list_blobs:
            destination_file_name = '{}/{}'.format(export_folder, blob)
            # download_blob(bucket_name, blob, destination_file_name)
        

        dir_updated = '{}/{}'.format(update_folder, prefix)
        if not os.path.exists(dir_updated):
            os.makedirs(dir_updated)

        report_columns_store = ['store_name', 'diff (%)', 'date', 'updated', 'original']
        df_summary_report_store = pd.DataFrame(columns=report_columns_store)

        files_list = os.listdir('{}/{}'.format(export_folder, prefix))

        for i in range(0, len(files_list) - 1):
            destination_file_name_past =  '{}/{}/{}'.format(export_folder, prefix, files_list[i])
            destination_file_name_current = '{}/{}/{}'.format(export_folder, prefix, files_list[i+1])

            df_current = pd.read_csv(destination_file_name_current)[compare_columns].drop_duplicates(subset='product_code')
            df_past = pd.read_csv(destination_file_name_past)[compare_columns].drop_duplicates(subset='product_code')

            df_updated, df_diff = compare(df_current, df_past, compare_columns)
            
            destination_file_name_updated = '{}/{}-{}'.format(dir_updated, update_folder, files_list[i+1])
            df_updated.to_csv(destination_file_name_updated)        

            destination_file_name_diff = '{}/{}-{}'.format(dir_updated, 'diff', files_list[i+1])
            df_diff.to_csv(destination_file_name_diff)

            df_report = report(df_updated, df_current, store_name=prefix)
            df_report['date'] = files_list[i+1].split('T')[0]
            df_summary_report_store = df_summary_report_store.append(df_report)
            df_summary_report_store.to_csv('summary-report-{}.csv'.format(prefix))
        
        df_summary_report_store.to_csv('summary-report-{}.csv'.format(prefix))

