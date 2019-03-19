import os, pytest, sys

import mock
from lanlytics_cloud_utils.aws import ec2_utils as ec2

class TestEC2Utils:
    @mock.patch('boto3.resource')
    def test_launch_ec2_instances(self, mock_resource):
        mock_resource.return_value.create_instances.return_value = [mock.MagicMock(), mock.MagicMock()]
        instances = ec2.launch_instances('test', tags=['foo', 'bar'])
        assert(len(instances) == 2)

    @mock.patch('boto3.resource')
    def test_terminate_instances(self, mock_resource):
        mock_resource.return_value.create_instances.return_value = [mock.MagicMock(), mock.MagicMock()]
        instances = ec2.launch_instances('test', tags=['foo', 'bar'])
        ec2.terminate_instances(instances)
        for instance in instances:
            assert(instance.terminate.called)
