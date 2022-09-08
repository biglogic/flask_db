import boto3
from boto3.session import Session
import csv
from datetime import datetime

profileName = input("Profile_name : ")
fileName = input("file_name : ")
header = ['Group_name','aws_managed','inline_policy']
session = boto3.Session(profile_name=profileName)
iam = session.client('iam')
group = iam.list_groups()
list_inline = []
list_aws = []
listu = []

def checkj():
        for i in group['Groups']:
                inline_policy =   iam.list_group_policies(
                                GroupName=i['GroupName']
                                )
                for k in range(len(inline_policy['PolicyNames'])):
                        list_inline.append(inline_policy['PolicyNames'][k])

                aws_managed = iam.list_attached_group_policies(
                                        GroupName=i['GroupName']
                                )
                for j in range(len(aws_managed['AttachedPolicies'])):
                        list_aws.append(aws_managed['AttachedPolicies'][j]['PolicyName'])
                print(i['GroupName'],list_inline,list_aws)
                listu.append([i['GroupName'],list_inline[0:],list_aws[0:]])
                list_inline.clear()
                list_aws.clear()

def csv_(head,list_): 
  with  open(fileName+'.csv' , 'w' , encoding='UTF8') as f :
      csvwriter = csv.writer(f)
      csvwriter.writerow(head)   
      csvwriter.writerows(list_)            

checkj()
csv_(header,listu)
 
