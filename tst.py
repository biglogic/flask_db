import time
import boto3 
from datetime import datetime, timedelta

session = boto3.Session(aws_access_key_id = "AKIAUAUU6KLEVKSKGNTH",aws_secret_access_key= "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", region_name= 'us-west-2')
ec2 = session.client('ec2')
image_id = {}
dictionary = {}
def list_instances():
        instances = ec2.describe_instances(Filters=[{'Name':'tag:Ami_image', 'Values': ['Yes']}])
        for i in range(len(instances['Reservations'])):
                id =  instances['Reservations'][i]['Instances'][0]['InstanceId']
                for j in  range(len(instances['Reservations'][i]['Instances'][0]['Tags'])):
                    dictionary.update({instances['Reservations'][i]['Instances'][0]['Tags'][j]['Key']:instances['Reservations'][i]['Instances'][0]['Tags'][j]['Value']})
                    key_name = instances['Reservations'][i]['Instances'][0]['Tags'][j]['Key']
                    print(instances['Reservations'][i]['Instances'][0]['Tags'][j]['Key'])
                
                try:    
                    if dictionary['Name'] != " ":
                            image_id['instance_id'] = id
                            response = ec2.stop_instances(
                                                            InstanceIds=[
                                                                    id,
                                                            ]
                                                        )
                            create_image(image_id['instance_id'],dictionary['Name'])
                except:
                        image_id['instance_id'] = id
                        response = ec2.stop_instances(
                                                        InstanceIds=[
                                                                id,
                                                        ]
                                                    )
                        create_image(image_id['instance_id'],"---")                        

def create_image(id, name):
        # print(id) 
        # try:
           create_time = datetime.now()
           create_fmt = create_time.strftime('%Y-%m-%d')
           response =  ec2.create_image(
                       InstanceId= id ,
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
           print(response['ImageId']) 
           check_image_status(response['ImageId'],id)
        #    image_id.append(response['ImageId'])                     
        # except:
        #     print("exception")     
                    
def check_image_status(img_id,ID):
    image = ec2.describe_images(ImageIds=[img_id])
    print(image['Images'][0]['State'])
    if image['Images'][0]['State']  == 'pending':
        time.sleep(5)
        print("wait")
        check_image_status(img_id,ID)
    elif image['Images'][0]['State'] == 'available':
        print(img_id)
        older_image(ID)
         
def older_image(ID):
     response = ec2.start_instances(
                                        InstanceIds=[
                                              ID,
                                        ]
                                    )    
                                         
             
list_instances()
