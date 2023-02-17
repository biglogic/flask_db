from tracemalloc import Snapshot
import boto3 
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader

profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
boto3.setup_default_session(profile_name = profileName)
ec2 = boto3.client('ec2' , region_name = region)
list_name = {}




# Open the file and load the file
with open('data.yml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    for i in data['inctance_id']:
        instances = ec2.describe_instances(InstanceIds=[i])
        # print(instances["Reservations"][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId'])
        # print(instances["Reservations"][0]['Instances'][0]['Placement']['AvailabilityZone'])
        # for j in instances["Reservations"][0]['Instances'][0]['Tags']:
        #     # print(j)
        #     list_name[j['Key']] = j['Value']
        # # print(list_name)    
        # if 'Name' in list_name:
        #             print(list_name['Name'])
        #             list_name.clear()
                
        # else:
        #           print("---")
        #           list_name.clear()        
        #         for j in instances["Reservations"][0]['Instances'][0]['Tags'][count]:
        #              print(j['Key'])

        snapshot = ec2.create_snapshot(
                                        Description= i+'-snapshot',
                                        VolumeId=instances["Reservations"][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId'],
                                        TagSpecifications=[
                                            {
                                                'ResourceType': 'snapshot',
                                                'Tags': [
                                                    {
                                                        'Key': 'Name',
                                                        'Value': i+'-snapshot'
                                                    },
                                                ]
                                            },
                                        ],
                                        DryRun=False
                                    )
        print(snapshot["SnapshotId"])     

# def volume_details():
#         response1 = ec2.describe_volumes(
#                                 VolumeIds=[
#                                    'vol-047584829733f0001' ,
#                                 ]
#                             )
#         print(response1['Volumes'][0]['AvailabilityZone'],response1['Volumes'][0]['Iops'],response1['Volumes'][0]['VolumeType'],response1['Volumes'][0]['Throughput'])                    
        #create_volume(response1['Volumes'][0]['AvailabilityZone'],response1['Volumes'][0]['Iops'],response1['Volumes'][0]['VolumeType'],response1['Volumes'][0]['Throughput'])



# def create_volume(AZ,IOP,Volumetype,throughput):
#             response = ec2.create_volume(
#                                 AvailabilityZone=AZ, 
#                                 SnapshotId= 'snap-01f48cf22467571e2',
#                                 VolumeType=Volumetype,
#                                 Iops=IOP,
#                                 Throughput=throughput
#                             )
#             print(response)

           