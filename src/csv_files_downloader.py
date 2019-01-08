import argparse
import datetime
import os
from pprint import pprint

from google.cloud import storage


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    list_blobs = []
    for blob in blobs:
        list_blobs.append(blob.name)
    return list_blobs

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)
    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def get_blob_name_by_index(bucket_name, prefix, index=-1):
    """Get blob name from list by index"""
    list_blobs = list_blobs_with_prefix(bucket_name, prefix)
    blob_name = list_blobs[index] if list_blobs else None
    return blob_name

def create_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)
    
def download_csv_files(bucket_name, prefix, list_index, export_folder):
    for index in list_index:
        source_blob_name = get_blob_name_by_index(bucket_name, prefix, index)
        print('###### source_blob_name >>>> ', source_blob_name)
        destination_file_name = '{}/{}'.format(export_folder, source_blob_name)
        print('###### destination_file_name >>>> ', destination_file_name)
        download_blob(bucket_name, source_blob_name, destination_file_name)

# if __name__ == "__main__":
#     bucket_name = 'pricetrolley-prod_scraper'
#     prefix = 'redmart'
#     list_index = [-1, -2]
#     export_folder = 'export'
#     dir_folder = '{}/{}'.format(export_folder, prefix)

#     create_folder(dir_folder)
#     download_csv_files(bucket_name, prefix, list_index, export_folder)
    
    
