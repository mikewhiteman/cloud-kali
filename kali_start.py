import boto3
import secrets
import string

ec2 = boto3.resource('ec2')

def generate_creds():
    alphabet = string.ascii_letters + string.digits
    username = 'cloudkali'
    password = ''.join(secrets.choice(alphabet) for i in range(12))
    return username, password
    
def create_instance(username, password):

    userdata = f"""#!/bin/bash
    ###
    # This script will provision an an account with a random password
    ###
    useradd -m -s /bin/bash {username}
    echo {username}:{password} |  chpasswd
    usermod -aG sudo {username}
    """

    ec2_instance = ec2.create_instances(
        ImageId='ami-0f24d5a5c0b5c0a18',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.small',
        KeyName='cis4093_kali_hosts',
        SecurityGroupIds=['sg-0eb2588803e7caef8'],
        UserData = userdata,
        SubnetId='subnet-021de55c66cc45ff3'
    ) 

    return ec2_instance

if __name__ == "__main__":
    username, password = generate_creds()
    instance = create_instance(username,password)
    print(f'[Debug] Created instance {instance} with username: {username} and password of {password}')