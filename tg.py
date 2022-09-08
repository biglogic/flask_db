import boto3
import csv


profileName = input("Profile_name : ")

session = boto3.Session(profile_name=profileName , region_name="us-east-1")
client = session.client('elb')
classic = client.describe_load_balancers(PageSize=400)
alb = session.client('elbv2')
ec2 = session.client('ec2')
instanceids = []
header = ["NAME"]
tg_list = []

def gettargetgroupname():
    tgs=alb.describe_target_groups()
    for i in range(len(tgs["TargetGroups"])):
        if len(tgs["TargetGroups"][i]["LoadBalancerArns"]) == 0 :
            #  print(tgs["TargetGroups"][i]["TargetGroupArn"])
             gettargethealth(tgs["TargetGroups"][i]["TargetGroupArn"],tgs["TargetGroups"][i]["TargetGroupName"])

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


def gettargethealth(arn,name):
    inss=alb.describe_target_health(TargetGroupArn=arn)
    # print(len(inss["TargetHealthDescriptions"]))
    print(inss['TargetHealthDescriptions'])
    if len(inss['TargetHealthDescriptions']) == 0 :
                 tg_list.append([name])
    #            print(tg_list)



def csv_(head,list_): 
  with  open('non_lb_list.csv' , 'w' , encoding='UTF8') as f :
      csvwriter = csv.writer(f)
      csvwriter.writerow(head)    
      csvwriter.writerows(list_)            
      tg_list.clear()

gettargetgroupname() 
csv_(header,tg_list)  