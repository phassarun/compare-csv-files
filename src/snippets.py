import os

from google.cloud import storage
import re


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    return [blob.name for blob in blobs]

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    splited_destination_file_name = destination_file_name.split('/')
    destination_store_name = '{}/{}'.format(splited_destination_file_name[0], splited_destination_file_name[1])
    if not os.path.exists(destination_store_name):
        os.makedirs(destination_store_name)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)
    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))
    return destination_file_name
    
def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    return [blob.name for blob in blobs]

def get_prefix_list(bucket_name):
    return set(map(lambda blob_name: blob_name.split('/')[0], list_blobs(bucket_name)))

def filter_by_country_code(blobs, country_code):
    return list(filter(lambda blob: country_code in blob, blobs))

def is_lang(blobs, country_code):
    for blob in blobs:
        if country_code in blob:
            return True
    return False
