import boto3

def launch_instances(image_id, **kwargs):
    ec2 = kwargs.get('ec2', None)
    if ec2 is None:
        ec2 = boto3.resource('ec2')
    instances = ec2.create_instances(ImageId=image_id,
                                     MinCount=1,
                                     MaxCount=kwargs.get('num_instances', 1),
                                     InstanceType=kwargs.get('instance_type', 't2.micro'),
                                     SecurityGroups=kwargs.get('security_groups', []),
                                     IamInstanceProfile=kwargs.get('role', None),
                                     UserData=kwargs.get('user_data', ''))
    tags = kwargs.get('tags', [])
    if len(tags) > 0:
        try:
            for instance in instances:
                instance.create_tags(Tags=tags)
        except Exception as e:
            print('Tag creation failed: {}'.format(e))
    return instances


def terminate_instances(instances):
    for instance in instances:
        instance.terminate()
