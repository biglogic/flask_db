import boto3
from boto3.session import Session
import csv
from datetime import datetime


session = boto3.Session(profile_name=name, region_name='us-east-1')
iam = session.client('ec2')
age = iam.describe_instances()
header = ['instance_Name', 'Instance_ip' ,'instance_id' , 'Instance_state']
list_stop = []

def list_instance():
    for i in range(len(age['Reservations'])) :
    #   print(age['Reservations'][i]['Instances'])  
      if age['Reservations'][i]['Instances'][0]['State']['Name'] == 'stopped':
        for j in range(len(age['Reservations'][i]['Instances'][0]['Tags'])):
           if age['Reservations'][i]['Instances'][0]['Tags'][j]['Key'] == 'Name' :
               print(age['Reservations'][i]['Instances'][0]['Tags'][j]['Key'], age['Reservations'][i]['Instances'][0]['Tags'][j]['Value'])
               list_stop.append([age['Reservations'][i]['Instances'][0]['Tags'][j]['Value'],age['Reservations'][i]['Instances'][0]['PrivateIpAddress'],age['Reservations'][i]['Instances'][0]['InstanceId'], age['Reservations'][i]['Instances'][0]['State']['Name']])


# def csv_(head,list_): 
#   with  open('stopinstace_list.csv' , 'w' , encoding='UTF8') as f :
#       csvwriter = csv.writer(f)
#       csvwriter.writerow(head)    
#       csvwriter.writerows(list_)            
#       list_stop.clear()

list_instance()
# csv_(header,list_stop) 