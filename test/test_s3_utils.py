import os, pytest, sys

sys.path.append('')

import mock
from aws_utils import s3_utils as s3
from collections import namedtuple
from io import BytesIO


def mock_list_files(uri, suffix='', s3=None):
    if uri.endswith('txt'):
        input_files = [uri]
    else:
        input_files = ['{}/{}.txt'.format(uri, f) for f in ['foo', 'bar', 'baz']]
    for f in input_files:
        yield f

def mock_download_fileobj(key, data):
    data.write(b'{"foo": "bar"}')

class TestS3Utils:
    def setup_method(self, _):
        self.uri = 's3://bucket/path/to/folder/file.txt'
        self.folder_uri = 's3://bucket/path/to/folder'
        self.local_file = '/path/to/folder/file.txt'
        self.local_folder = '/path/to/folder'

    def test_split_s3_uri(self):
        bucket_name, key = s3.split_s3_uri(self.uri)
        assert(bucket_name == 'bucket')
        assert(key == 'path/to/folder/file.txt')

    @mock.patch('boto3.resource')
    def test_parse_s3_uri(self, mock_resource):
        bucket, key = s3.parse_s3_uri(self.uri)
        assert(key == 'path/to/folder/file.txt')

    @mock.patch('boto3.resource')
    @mock.patch('aws_utils.s3_utils.list_files_s3', side_effect=mock_list_files)
    def test_download_from_s3(self, mock_list, mock_resource):
        s3.download_from_s3(self.uri, self.local_file)

    @mock.patch('boto3.resource')
    @mock.patch('os.listdir', return_value=['file.txt'])
    def test_upload_to_s3(self, mock_list_dir, mock_resource):
        s3.upload_to_s3(self.local_file, self.uri)

    @mock.patch('boto3.resource')
    def test_stream_from_s3(self, mock_resource):
        mock_resource.Bucket.return_value.download_fileobj.side_effect = mock_download_fileobj
        result = s3.stream_from_s3(self.uri, s3=mock_resource)
        assert(result == '{"foo": "bar"}')

    @mock.patch('boto3.resource')
    def test_stream_from_s3_json(self, mock_resource):
        mock_resource.Bucket.return_value.download_fileobj.side_effect = mock_download_fileobj
        result = s3.stream_from_s3(self.uri, s3=mock_resource, json=True)
        assert(result == {'foo': 'bar'})

    @mock.patch('boto3.resource')
    def test_stream_to_s3(self, mock_resource):
        s3.stream_to_s3(BytesIO(), self.uri)

    @mock.patch('boto3.resource')
    def test_list_files_s3(self, mock_resource):
        Obj = namedtuple('Obj', ['key'])
        mock_resource.Bucket.return_value.objects.filter.side_effect = [[Obj(key='foo')], [Obj(key='bar')], []]
        result = [uri for uri in s3.list_files_s3(self.uri, s3=mock_resource)]
        assert(len(result) == 2)
