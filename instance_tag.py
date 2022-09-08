import boto3
from boto3.session import Session
import csv
from datetime import datetime

profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
session = boto3.Session(profile_name=profileName,region_name=region)
age = session.resource('iam')
iam = session.client('iam')
instance = session.client("ec2")
count = 0
groups = []
List_user = []
time = []
header = ['UserName']
data = []
list2 = []
lastActivity = []
age_day = []
dictionary= {}


# def instance_list():
#     response = instance.describe_instances(
#       Filters=[
#         {
#             'Name': 'tag:Stage',
#             'Values': [
#                 'stg',
#             ]
#         }
#       ]
#      )
#     list_(response)

# def list_(val):
#     for i in range(len(val["Reservations"])):
#         #print(val["Reservations"][i]['Instances'][0]['InstanceId'],val["Reservations"][i]['Instances'][0]['Tags'])
#          for j in range(len(val["Reservations"][i]['Instances'][0]['Tags'])):
#              if  val["Reservations"][i]['Instances'][0]['Tags'][j]["Key"] == 'Name':
#                      print(val["Reservations"][i]['Instances'][0]['InstanceId'],val["Reservations"][i]['Instances'][0]['Tags'][j]["Value"])                   

# instance_list()
def find_user_and_groups():
        for userlist in iam.list_users()['Users']:
            userGroups = iam.list_groups_for_user(UserName=userlist['UserName'])
            try:  
              get_group_list(userlist['UserName'],userGroups['Groups'],userlist['CreateDate'],userlist['PasswordLastUsed'])
            except:
              get_group_list(userlist['UserName'],userGroups['Groups'],userlist['CreateDate'],"N/A")
   



def get_group_list(userlist,group,date,password):
    response = iam.list_mfa_devices(UserName=userlist)
    if  not response['MFADevices']:
      for groupNames in group:
        name = groupNames['GroupName']
        groups.append(name) 
      get_acess_key(userlist,groups,date,password ,"No_MFA")    
    else: 
      for groupNames in group:
        name = groupNames['GroupName']
        groups.append(name) 
      get_acess_key(userlist,groups,date,password ,"MFA_Exist")

def get_acess_key (userlist,group_list,usercreate,password,mfa_status):    
        paginator = iam.get_paginator('list_access_keys')
        for response in paginator.paginate(UserName=userlist):
            accessKeyMetadata = response['AccessKeyMetadata']
            if len(accessKeyMetadata) != 0 : 
                # print(len(accessKeyMetadata))
                for i in range(len(accessKeyMetadata)):              
                       if  accessKeyMetadata[i]['Status'] == 'Active' :
                           print(accessKeyMetadata[i]['UserName'])
                           password_age(accessKeyMetadata[i]['UserName'])
                           break
            else:
                password_age(userlist)
                print(userlist)

            # if len(accessKeyMetadata) == 1 : 
            #   List_user.append([userlist,str(usercreate),password,time[0], "N/A", lastActivity[0] , 'N/A' , mfa_status , age_day[0],group_list[0:]])
            #   groups.clear()
            #   age_day.clear()
            #   time.clear()
            #   lastActivity.clear()
            # elif len(accessKeyMetadata) == 0 :
            #   List_user.append([userlist,str(usercreate),password,"N/A", "N/A", "N/A"  , "N/A"  , mfa_status ,age_day[0], group_list[0:]])
            #   groups.clear()
            #   age_day.clear()
            #   time.clear()
            #   lastActivity.clear()  
            # else:
            #   List_user.append([userlist,str(usercreate),password,time[0],time[1], lastActivity[0] ,lastActivity[1] , mfa_status ,age_day[0],group_list[0:]])
            #   groups.clear()
            #   age_day.clear()
            #   time.clear()
            #   lastActivity.clear()  
            
            

def  password_age(val): 
     try: 
        # age1 = age.LoginProfile(val)
        # age2 = age1.create_date
        # print("true")
        response = iam.get_login_profile(UserName=val)
        # List_user.append([val])
     except Exception as e:
        if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
            # List_user.append(['User {} has no login profile'.format(val)])
            List_user.append([val])
            print('User {} has no login profile'.format(val))

    #  except:
    #    age_day.append('None')      

def csv_(head,list_): 
  with  open(fileName+'.csv' , 'w' , encoding='UTF8') as f :
      csvwriter = csv.writer(f)
      csvwriter.writerow(head)
    #   print(List_user)    
      csvwriter.writerows(list_)            
      groups.clear()
      time.clear()
      age_day.clear()





find_user_and_groups()  
csv_(header,List_user)




