import json
from multiprocessing.connection import wait
from time import sleep
from jinja2 import Template
from tracemalloc import Snapshot
import boto3 , json
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader

profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
boto3.setup_default_session(profile_name = profileName)
ec2 = boto3.client('ec2' , region_name = region)
volume_id = []
Volume_name = []

def volume_details(id,snapid):
        response1 = ec2.describe_volumes(
                                VolumeIds=[
                                   id ,
                                ]
                            )
        print(response1['Volumes'][0]['AvailabilityZone'],response1['Volumes'][0]['Iops'],response1['Volumes'][0]['VolumeType'],response1['Volumes'][0]["Tags"][0]['Value'])
        sleep(22)                   
        create_volume(snapid,response1['Volumes'][0]['AvailabilityZone'],response1['Volumes'][0]['Iops'],response1['Volumes'][0]['VolumeType'],125,response1['Volumes'][0]["Tags"][0]['Value'])




def create_volume(id,AZ,IOP,Volumetype,throughput,name):
            response = ec2.create_volume(
                                AvailabilityZone=AZ, 
                                SnapshotId= id,
                                VolumeType=Volumetype,
                                #Iops=IOP,
                                #Throughput=throughput
                                TagSpecifications=[
                                        {
                                            'ResourceType': 'volume',  
                                            'Tags': [
                                                {
                                                    'Key': 'Name',
                                                    'Value': name
                                                },
                                            ]
                                        }
                                    ]
                            )
            volume_id.append(response['VolumeId'])
            Volume_name.append(name)                
            

def create_json(namel,idl):
    print("ok")
    f = open("data1.json", "w")
    tm = Template("""
{
    "kubernetes":[
         { "ns":"",
           "kube_service" : "",
           "pvcname":[""],
           "pvname":{{name}},
           "storage":[""],
           "storageclaim":[""],
           "storageclassName":[""],
           "kskind":"",
           "fstype":[""],
           "volumeId":{{id}},
           "replicas":"" 
         }
     ]
 }
    """)
    msg = tm.render(id=json.dumps(idl),name=json.dumps(namel))                
    f.write(msg)
    f.close()       

# Open the file and load the file
with open('data.yml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    for i in data['inctance_id']:
        snapshot = ec2.create_snapshot(
                                        Description=i+"snapshot",
                                        VolumeId=i,
                                        TagSpecifications=[
                                            {
                                                'ResourceType': 'snapshot',
                                                'Tags': [
                                                    {
                                                        'Key': 'Name',
                                                        'Value': i+'-snapshot'
                                                    },
                                                ]
                                            },
                                        ],
                                        DryRun=False
                                    )
        print(snapshot["SnapshotId"])  
        volume_details(i,snapshot["SnapshotId"])                                                 

create_json(volume_id,Volume_name)
           