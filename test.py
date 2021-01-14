import boto3
import json

client = boto3.client('ec2')
response = client.describe_instances(
    InstanceIds=['i-05f56a3bc860d868a'])

print(response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp'])