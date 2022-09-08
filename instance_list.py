import boto3
from boto3.session import Session
import csv
# from datetime import datetime
name = input("please enter profile Name : ")
session = boto3.Session(profile_name=name, region_name='us-east-1')
iam = session.client('ec2')
age = iam.describe_instances()
alarams = session.client('cloudwatch')
alaram = alarams.describe_alarms()
header = ['instance_Name', 'Instance_ip' ,'instance_id' , 'Alarm']
list_stop = []
list_dimensions = []
dictionary = {}
def alarm_dimension():
  for k in range(len(alaram['MetricAlarms'])):
      # print(len(alaram['MetricAlarms'][k]['Dimensions']))
      for l in range(len(alaram['MetricAlarms'][k]['Dimensions'])):
        # print(alaram['MetricAlarms'][k]['Dimensions'][l]['Name'],alaram['MetricAlarms'][k]['Dimensions'][l]['Value'])
        if  alaram['MetricAlarms'][k]['Dimensions'][l]['Name'] == 'InstanceId' or alaram['MetricAlarms'][k]['Dimensions'][l]['Name'] == 'Instance':
          print(alaram['MetricAlarms'][k]['Dimensions'][l]['Value'])
          if alaram['MetricAlarms'][k]['Dimensions'][l]['Value'] not in list_dimensions:
               list_dimensions.append(alaram['MetricAlarms'][k]['Dimensions'][l]['Value'])
  print(list_dimensions)
  list_instance()

def list_instance():
    for i in range(len(age['Reservations'])) :
        for j in age['Reservations'][i]['Instances'][0]['Tags'][0:]:
              dictionary.update({j['Key']:j['Value']})
        print(dictionary.keys())
        try:   
            if dictionary['Name'] != " ":  
              if age['Reservations'][i]['Instances'][0]['InstanceId'] not in list_dimensions:
                      print(dictionary['Name'], j['Value'])
                      list_stop.append([dictionary['Name'],age['Reservations'][i]['Instances'][0]['InstanceId'], "None"])
                      dictionary.clear()  
        except:     
            if age['Reservations'][i]['Instances'][0]['InstanceId'] not in list_dimensions:
                  list_stop.append(["----",age['Reservations'][i]['Instances'][0]['InstanceId'], "None"])
                  dictionary.clear() 
              # print(age['Reservations'][i]['Instances'][0]['Tags'][0:].Keys)          

def csv_(head,list_): 
  with  open('instace_Alarm_enabled_list.csv' , 'w' , encoding='UTF8') as f :
      csvwriter = csv.writer(f)
      csvwriter.writerow(head)    
      csvwriter.writerows(list_)            
      list_stop.clear()

alarm_dimension()
csv_(header,list_stop) 
