from logging import error
from tracemalloc import Snapshot
import boto3 
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader

profileName = input("Profile_name : ")
region = input("region : ")
# fileName = input("file_name : ")
boto3.setup_default_session(profile_name = profileName)
snap = boto3.client('ec2' , region_name = region)
list_name = {}
list_tags = {}
volumes_tags = {}
volume_list = []
not_available = {}

# def copysnap(id):
#         with open('snapdata.yml') as f:
#             data = yaml.load(f, Loader=SafeLoader)
            
#             for i in data['snap_id']:
#                 try:
#                    response2 = snap.copy_snapshot(
                        #  Description='string
#                        TagSpecifications=[
#                                  {
#                                     'ResourceType': 'snapshot',
#                                     'Tags': [
#                                         {
#                                             'Key': "Name",
#                                             'Value': list_tags["Name"]
#                                         },
#                                     ]
#                                 },
#                             ],
#                         SourceSnapshotId=id,
#                         SourceRegion='us-east-1',
#                         Encrypted=True   
#                    )
#                    print(response2)
#                 except:
#                     response2 = snap.copy_snapshot(
#                        TagSpecifications=[
#                                 {
#                                     'ResourceType': 'volume',
#                                 }
#                             ],
#                         Encrypted=True,
#                         SourceSnapshotId=id,
#                         SourceRegion='us-east-1'   

#                    )

# with open('snapdata.yml') as f:
#   data = yaml.load(f, Loader=SafeLoader)
#   for i in data['snap_id']:
#     try:    
#         response = snap.describe_snapshots(
#             SnapshotIds=[i]
#         )
#         if response['Snapshots'][0]['Encrypted'] == False :
#             try:
#                 for j in  range(len(response['Snapshots'][0]['Tags'])):
#                     list_tags[response['Snapshots'][0]['Tags'][j]['Key']] = response['Snapshots'][0]['Tags'][j]['Value']
#                 if 'aws:backup:source-resource' in list_tags:
#                     try: 
#                             response1 = snap.describe_volumes(
#                                                     VolumeIds=[
#                                                     response['Snapshots'][0]['VolumeId'] ,
#                                                     ]
#                                                 )
#                             print(i + " not Done")
#                             list_tags.clear()
                                
#                     except:
#                         print(i + " not Done")
#                         volumes_tags[response['Snapshots'][0]['VolumeId']] = i
#                         # print(response['Snapshots'][0]['VolumeId']+" not Present") 
#                         list_tags.clear()
#                 else:
#                     try: 
#                             response1 = snap.describe_volumes(
#                                                     VolumeIds=[
#                                                     response['Snapshots'][0]['VolumeId'] ,
#                                                     ]
#                                                 )
#                             # print(response['Snapshots'][0]['VolumeId'])
#                             print(list_tags[0:],i)
#                             list_tags.clear()    
#                     except:
#                         print(i+" notDone")
#                         volumes_tags[response['Snapshots'][0]['VolumeId']] = i
#                         list_tags.clear()
#             except:
#                  try: 
#                             response1 = snap.describe_volumes(
#                                                     VolumeIds=[
#                                                     response['Snapshots'][0]['VolumeId'] ,
#                                                     ]
#                                                 )
#                             volumes_tags[response['Snapshots'][0]['VolumeId']] = i
#                             list_tags.clear()
#                             # print(volumes_tags.keys(),volumes_tags.values())
#                             if response['Snapshots'][0]['Description'] == '':
#                                snap.delete_snapshot(SnapshotId=i)
#                                print(response['Snapshots'][0]['Description'])
#                                print(i+ "  Done " + response['Snapshots'][0]['VolumeId']) 
#                             else: 
#                                  print(i+ " not Done")   
   
                                
#                  except:
#                         volumes_tags[response['Snapshots'][0]['VolumeId']] = i
#                         # print(volumes_tags.keys())
#                         print(i +" not Done")
#                         print(response['Snapshots'][0]['Description'])
#                         list_tags.clear()
#     except:
#         # print(volumes_tags.keys(),volumes_tags.values())
#         # print(i ," Done")
#         pass
#   print(volumes_tags) 

# print(volumes_tags.keys(),volumes_tags.values())


# #         # if response['Snapshots'][0]['Encrypted'] == False :
# #         #    print("step1") 
# #         #    for j in  range(len(response['Snapshots'][0]['Tags'])):
# #         #         list_tags[response['Snapshots'][0]['Tags'][j]['Key']] = response['Snapshots'][0]['Tags'][j]['Value']
# #         #         if 'Name' in list_tags:
# #         #             #copysnap(i)
# #         #             print("start")





with open('snapdata.yml') as f:
  data = yaml.load(f, Loader=SafeLoader)
  for i in data['snap_id']:
    try:  
        response = snap.describe_snapshots(
             SnapshotIds=[i]
        )
        print("UNDONE")
    except:
        print("Done")