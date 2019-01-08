from src.csv_files_downloader import download_csv_files

export_folder = 'export'
bucket_name = 'pricetrolley-prod_scraper'
prefix = 'redmart'
list_index = [-1, -2]
download_csv_files(bucket_name, prefix, list_index, export_folder)
