from src import csv_files_downloader

bucket_name = 'pricetrolley-prod_scraper'
prefix = 'redmart'
list_index = [-1, -2]
export_folder = 'export'
dir_folder = '{}/{}'.format(export_folder, prefix)

csv_files_downloader.create_folder(dir_folder)
csv_files_downloader.download_csv_files(bucket_name, prefix, list_index, export_folder)
