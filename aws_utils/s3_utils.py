import boto3
import os
import ujson
from io import BytesIO


def split_s3_uri(uri):
    return uri.split('/', 3)[2:]


def parse_s3_uri(uri, s3=None):
    if s3 is None:
        s3 = boto3.resource('s3')
    bucket_name, key = split_s3_uri(uri)
    return s3.Bucket(bucket_name), key


def download_from_s3(uri, local_file, s3=None):
    if s3 is None:
        s3 = boto3.resource('s3')
    bucket, prefix = parse_s3_uri(uri, s3)
    for obj in list_files_s3(uri, s3=s3):
        bucket_name, key = split_s3_uri(obj)
        local_file = os.path.join(os.path.dirname(local_file), 
                                  os.path.basename(key))
        if not key.endswith('/'):
            bucket.download_file(key, local_file)


def upload_to_s3(local_file, uri, s3=None):
    if s3 is None:
        s3 = boto3.resource('s3')
    bucket, key = parse_s3_uri(uri, s3)
    local_dir = os.path.dirname(local_file)
    prefix = os.path.basename(local_file)
    for f in os.listdir(local_dir):
        filename, ext = os.path.splitext(f)
        if f == prefix:
            bucket.upload_file(local_file, key)
            break
        elif filename == prefix:
            bucket.upload_file(local_file + ext, key + ext)


def stream_from_s3(uri, s3=None, json=False):
    if s3 is None:
        s3 = boto3.resource('s3')
    bucket, key = parse_s3_uri(uri, s3)
    data = BytesIO()
    try:
        bucket.download_fileobj(key, data)
        if json is True:
            result = ujson.loads(data.getvalue())
        else:
            result = data.getvalue().decode()
        return result
    except Exception as e:
        print('Failed to load {}'.format(uri))
    finally:
        data.close()


def stream_to_s3(stream, uri, s3=None):
    if s3 is None:
        s3 = boto3.resource('s3')
    bucket, key = parse_s3_uri(uri, s3)
    bucket.upload_fileobj(stream, key)
    return uri


def list_files_s3(uri, suffix='', s3=None):
    if s3 is None:
        s3 = boto3.resource('s3')
    bucket, prefix = parse_s3_uri(uri, s3)
    input_files = ['']
    while len(input_files) > 0:
        input_files = [obj.key
                        for obj in bucket.objects.filter(Prefix=prefix, Marker=input_files[-1])
                        if obj.key.endswith(suffix)]
        for f in input_files:
            yield os.path.join('s3://{}'.format(bucket.name), f)


