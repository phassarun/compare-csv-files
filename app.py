import pandas as pd

from src.comparison import compare_csv_files, create_csv_from_dataframe
from src.csv_files_downloader import download_csv_files

if __name__ == "__main__":
    export_folder = 'export'
    update_folder = 'updated'
    bucket_name = 'pricetrolley-prod_scraper'
    prefix = 'redmart'
    list_index = [-1, -2] # -1 is current file, -2 is past file

    path_csv_files = download_csv_files(bucket_name, prefix, list_index, export_folder)
    df_updated = compare_csv_files(path_csv_files[0], path_csv_files[1])
    
    path_output_csv = '{}/{}'.format(update_folder, prefix)
    create_csv_from_dataframe(df_updated, path_output_csv)
