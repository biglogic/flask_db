import boto3 
from datetime import datetime, timedelta

profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
boto3.setup_default_session(profile_name = profileName)
ec2 = boto3.client('ec2' , region_name = region)
image_id = {}
def lambda_handler():
        instances = ec2.describe_instances(Filters=[{'Name':'tag:Ami_image', 'Values': ['True']}])
        for i in range(len(instances['Reservations'])):
                id =  instances['Reservations'][i]['Instances'][0]['InstanceId']
                for j in  range(len(instances['Reservations'][i]['Instances'][0]['Tags'])):
                    key_name = instances['Reservations'][i]['Instances'][0]['Tags'][j]['Key']
                    if key_name == 'Name':
                         image_id['instance_id'] = id
                         image_id['Value'] = instances['Reservations'][i]['Instances'][0]['Tags'][j]['Value']
                         create_image(image_id['instance_id'],image_id['Value'])
                
                
def create_image(id, name):
        try:
           create_time = datetime.now()
           create_fmt = create_time.strftime('%Y-%m-%d')
           response =  ec2.create_image(
                       InstanceId= id,
                       Name= "Lambda - " + id + " from " + create_fmt,
                       NoReboot=False
                          
                    )
           tag = ec2.create_tags(
                                    DryRun=False,
                                    Resources=[
                                        response['ImageId']
                                    ],
                                    Tags=[
                                        {
                                            'Key': 'Name',
                                            'Value': name
                                        },
                                        {
                                            'Key' : 'Retention',
                                            'Value': '7'
                                            
                                        },
                                        {
                                            'Key': 'Created_by',
                                            'Value': 'Lambda'
                                        }
                                    ]
                                )            
             
        except:
           print("unable to run")     
                    

lambda_handler()                    
