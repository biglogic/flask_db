from email.header import Header
import os, boto3
from prompt_toolkit import Application
import csv


profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
session = boto3.Session(profile_name=profileName , region_name=region)
client = session.client('ec2')

response1 = client.describe_nat_gateways()

list_Nat = []
header = ["NAT_ID","STATE","ROUTE_TABLE"]

for lenth in range(len(response1["NatGateways"])): 
       print(response1["NatGateways"][lenth]["State"])
       response = client.describe_route_tables(
           Filters=[
                {
                    'Name': 'route.nat-gateway-id',
                    'Values': [
                        response1["NatGateways"][lenth]['NatGatewayId'],
                    ]
                },
            ],
       )
       print(response)
       list_Nat.append([response1["NatGateways"][lenth]["NatGatewayId"],response1["NatGateways"][lenth]["State"],response['RouteTables'][0]['Associations'][0]["AssociationState"]['State']])

def csv_(head,list_): 
  with  open(fileName+'.csv' , 'w' , encoding='UTF8') as f :
      csvwriter = csv.writer(f)
      csvwriter.writerow(head)    
      csvwriter.writerows(list_)            
      list_Nat.clear()       

csv_(header,list_Nat)      