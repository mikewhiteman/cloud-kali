import boto3
ec2 = boto3.resource('ec2')

userdata = """#!/bin/bash
###
# This script will automatically generate accounts, provision random passwords, and add the accounts t>
###

function rand_pass {
 head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12 ; echo ''
}

usernames=("cat" "dog" "mouse" "llama" "horse")
echo "***Connection Information***"
echo "IP Address: $(curl http://169.254.169.254/latest/meta-data/public-ipv4)" 

for i in "${usernames[@]}"
do
    username=$i
    randompw=$(rand_pass)
    useradd -m -s /bin/bash $username
    echo $username:$randompw |  chpasswd
    usermod -aG sudo $username
    echo "User:" $username
    echo "Password:" $randompw 
done
"""


instances = ec2.create_instances(
     ImageId='ami-0f24d5a5c0b5c0a18',
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.small',
     KeyName='cis4093_kali_hosts',
     SecurityGroupIds=['sg-0eb2588803e7caef8'],
     UserData = userdata,
     SubnetId='subnet-021de55c66cc45ff3'
 ) 

print(instances)