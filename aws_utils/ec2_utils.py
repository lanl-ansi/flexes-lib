import boto3

def launch_ec2(image_id, num_instances=1, instance_type='t2.micro', security_groups=[],
                tags=[], roles=[]):
    ec2 = boto3.resource('ec2')
    instances = ec2.create_instances(ImageId=image_id,
                                     MinCount=1,
                                     MaxCount=num_instances,
                                     InstanceType=instance_type,
                                     SecurityGroups=security_groups,
                                     IamInstanceProfile=role)
    if len(tags) > 0:
        for instance in instances:
            instance.create_tags(Tags=tags)
    return instances


def terminate_instances(instance_ids):
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=instance_ids).terminate()
    return
