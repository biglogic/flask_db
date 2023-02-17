from tracemalloc import Snapshot
import boto3 
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader

profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
session = boto3.Session(profile_name=profileName, region_name=region)
iam = session.client('ec2')
paginator = iam.describe_volumes()

def check_type():
    count=0
    for i in range(len(paginator["Volumes"])): 
        # print(paginator["Volumes"][i]['VolumeId'])                                           
        if len(paginator["Volumes"][i]['Attachments']) == 0 and paginator["Volumes"][i]['Encrypted'] == False :
            count=count+1
            
            print("- " +paginator["Volumes"][i]['VolumeId'])                    


def describe_snap():
    with open('snapdetails.yml') as f:
       data = yaml.load(f, Loader=SafeLoader)
       for i in data["inctance_id"]:
        print(i+'-snap')   
        response = iam.describe_snapshots(
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            i+'-snapshot',
                        ]
                    },
                ]
        )
        if len(response['Snapshots']) != 0 :
          result = iam.delete_snapshot(SnapshotId=response['Snapshots'][0]['SnapshotId'])
          print(result)

#describe_snap()
check_type()        