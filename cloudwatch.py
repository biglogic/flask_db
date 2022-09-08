import boto3
from boto3.session import Session
import csv
# from datetime import datetime
name = input("please enter profile Name : ")
region = input("region : ")
fileName = input("file_name : ")
session = boto3.Session(profile_name=name, region_name=region)
iam = session.client('ec2')
age = iam.describe_instances()
alarams = session.client('cloudwatch')
alaram = alarams.describe_alarms()
paginator = alarams.get_paginator('describe_alarms')
response_iterator = paginator.paginate()

header = ['Alarm_Name', 'Metrics' ,'Threshold','Comparison_operator', 'Namespace' ]
list_stop = []
list_Alarm = []
dictionary = {}
# for k in range(len(response_iterator['MetricAlarms'])):
#         print(response_iterator['MetricAlarms'][k]['AlarmName'],response_iterator['MetricAlarms'][k]['MetricName'],response_iterator['MetricAlarms'][k]['Threshold'],response_iterator['MetricAlarms'][k]['ComparisonOperator'])

# print(alaram)
def alarm_dimension():
 for i in response_iterator:
    for k in range(len(i['MetricAlarms'])):
        print(i['MetricAlarms'][k])
        print(i['MetricAlarms'][k]['AlarmName'])
    
        # list_stop.append(response_iterator['MetricAlarms'][k]['AlarmName'])
        list_Alarm.append([i['MetricAlarms'][k]['AlarmName'],i['MetricAlarms'][k]['MetricName'],i['MetricAlarms'][k]['Threshold'],i['MetricAlarms'][k]['ComparisonOperator'],i['MetricAlarms'][k]['Namespace']])
#         if  alaram['MetricAlarms'][k]['Dimensions'][l]['Name'] == 'InstanceId' or alaram['MetricAlarms'][k]['Dimensions'][l]['Name'] == 'Instance':
#        #   print(alaram['MetricAlarms'][k]['Dimensions'][l]['Value'])
#           if alaram['MetricAlarms'][k]['Dimensions'][l]['Value'] not in list_dimensions:
#                list_dimensions.append(alaram['MetricAlarms'][k]['Dimensions'][l]['Value'])
#   print(list_dimensins)

def csv_(head,list_): 
  with  open(fileName+'.csv' , 'w' , encoding='UTF8') as f :
      csvwriter = csv.writer(f)
      csvwriter.writerow(head)    
      csvwriter.writerows(list_)            
      list_stop.clear()


alarm_dimension()
csv_(header,list_Alarm)