import boto3
from boto3.session import Session
import csv
from datetime import datetime
header = ["Volume_name","Volume_id","Previous_type","Current_type"] 
list_volume = []

profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
session = boto3.Session(profile_name=profileName, region_name=region)
iam = session.client('ec2')
paginator = iam.describe_volumes()
page_iterator = paginator["Volumes"]

def check_type():
    for i in page_iterator:
        print(i['VolumeType'])
        if i['VolumeType'] == 'gp2':
                try:
                  for j in range(len(i['Tags'])):
                    if i['Tags'][j]['Key'] == 'Name':
                       mod_volume(i['Tags'][j]['Value'],i['VolumeId'],i['VolumeType'])
                except:
                      mod_volume("---",i['VolumeId'],i['VolumeType'])   

def mod_volume(name,id,type):
        response = iam.modify_volume(
        DryRun=False,
        VolumeId=id,
        VolumeType='gp3'
        )
        print(response)
        list_volume.append([name,id,type,response['VolumeModification']['TargetVolumeType']])
      
def csv_(head,list_):
      with  open(fileName+'.csv' , 'w' , encoding='UTF8') as f :
        csvwriter = csv.writer(f)
        csvwriter.writerow(head)    
        csvwriter.writerows(list_)            
        list_volume.clear()


check_type()
csv_(header,list_volume)