from tracemalloc import Snapshot
import boto3 
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader

profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
boto3.setup_default_session(profile_name = profileName)
ec2 = boto3.client('ec2' , region_name = region)
list_name = {}



with open('datavol.yml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    for i in data['volume_id']:
        response = ec2.delete_volume(
               VolumeId=i
            )
        print(response)    