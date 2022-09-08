import os, boto3
from prompt_toolkit import Application
import csv

profileName = input("Profile_name : ")

session = boto3.Session(profile_name=profileName , region_name="us-east-1")
client = session.client('elb')
classic = client.describe_load_balancers(PageSize=400)
alb = session.client('elbv2')
ec2 = session.client('ec2')
lbs = alb.describe_load_balancers(PageSize=400)
print(classic['LoadBalancerDescriptions'][0])

status = []
lbName = []
lb_type = []
instanceids=[]
lbs_list = []
header = ["NAME","STATE","TYPE"]

def gettargetgroupname(arn):
    tgs=alb.describe_target_groups(LoadBalancerArn=arn)
    tgarns=[]
    for tg in tgs["TargetGroups"]:
        tgarns.append(tg["TargetGroupName"])
    return tgarns



def classic_lb():
  for lenth in range(len(classic["LoadBalancerDescriptions"])):
    print(classic["LoadBalancerDescriptions"][lenth]["Instances"])  
    if len(classic["LoadBalancerDescriptions"][lenth]["Instances"]) == 0 :
       lbs_list.append([classic["LoadBalancerDescriptions"][lenth]["LoadBalancerName"],"Not-Active","classic"])
    if len(classic["LoadBalancerDescriptions"][lenth]["Instances"]) != 0 :
       lbs_list.append([classic["LoadBalancerDescriptions"][lenth]["LoadBalancerName"],"Active","classic"])
  
  print(lbs_list)       

def gettargetgrouparns(arn):
    tgs=alb.describe_target_groups(LoadBalancerArn=arn)
    tgarns=[]
    for tg in tgs["TargetGroups"]:
        tgarns.append(tg["TargetGroupArn"])
    return tgarns

def getinstancename(instanceid):
    instances=ec2.describe_instances(Filters=[
        {
            'Name': 'instance-id',
            'Values': [
                instanceid
            ]
        },
    ],)
    for instance in instances["Reservations"]:
        for inst in instance["Instances"]:
            for tag in inst["Tags"]:
                if tag['Key'] == 'Name':
                    return (tag['Value'])

def gettargethealth(arn):
    inss=alb.describe_target_health(TargetGroupArn=arn)
    # print(len(inss["TargetHealthDescriptions"]))
    for ins in inss["TargetHealthDescriptions"]:
        ins["Name"]=getinstancename(ins['Target']['Id'])
        instanceids.append(ins['Target']['Id'])
    return instanceids

def application_lb():
    for lb in lbs["LoadBalancers"]:
        # print(len(gettargetgroupname(lb["LoadBalancerArn"])))
        if len(gettargetgroupname(lb["LoadBalancerArn"])) == 0   :
          lbs_list.append([lb["LoadBalancerName"],"No-TG",lb["Type"]])
        if len(gettargetgroupname(lb["LoadBalancerArn"])) != 0 :
            for tgs in gettargetgrouparns(lb["LoadBalancerArn"]):
                len(gettargethealth(tgs))

            if len(gettargethealth(tgs)) == 0:
                print(gettargethealth(tgs))
                print("\n"*2)
                print ("-"*6)
                print("Name:",lb["LoadBalancerName"])
                print("state:" , lb["State"]["Code"])
                print("Type:",lb["Type"])
                print("TargetGroups:",str(gettargetgroupname(lb["LoadBalancerArn"])))
                lbs_list.append([lb["LoadBalancerName"],"Not-Active",lb["Type"]])
                instanceids.clear()
            if len(gettargethealth(tgs)) != 0 :
                lbs_list.append([lb["LoadBalancerName"],"Active",lb["Type"]])
                instanceids.clear()

    csv_(header,lbs_list)   

def csv_(head,list_): 
  with  open('non_lb_list.csv' , 'w' , encoding='UTF8') as f :
      csvwriter = csv.writer(f)
      csvwriter.writerow(head)    
      csvwriter.writerows(list_)            
      lbs_list.clear()
print(gettargetgrouparns(lbs['LoadBalancers'][0]["LoadBalancerArn"]))

classic_lb()
application_lb()

