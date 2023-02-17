from ast import Delete
from logging import error
import re
from tracemalloc import Snapshot
import boto3 
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader

profileName = input("Profile_name : ")
region = input("region : ")
fileName = input("file_name : ")
boto3.setup_default_session(profile_name = profileName)
snap = boto3.client('ec2' , region_name = region)
list_name = {}
list_tags = {}
volumes_tags = {}
volume_list = []
not_available = {}

listofvolume=['vol-03e3217d8b6c12f80', 'vol-052affd2974e8e588', 'vol-05aa70f58b3e78747', 'vol-090814e7c1f8eb1fd', 'vol-09fbf5e1d00e1ae89', 'vol-02873d2bfb486dfec', 'vol-072919e47bfa7560a', 'vol-0161c50c13ac4bb37', 'vol-0451533f03c9947d4', 'vol-0021c9394b0555c21', 'vol-002ed08aa3806fe29', 'vol-06068ba79ad202c34', 'vol-07d5a8bc3289e4b72', 'vol-0bb9e25670189a9b0', 'vol-08f5d4da11cf4a1c2', 'vol-08051c6e05dd73a77', 'vol-0567e764c805c45d4', 'vol-0c2ac9b701c93b88a', 'vol-0f5ef3f95ff167547', 'vol-0fa572990cee3577c', 'vol-0fc697277f69b0984', 'vol-0d41177a0601acb7d', 'vol-07f9896bf811b50d1', 'vol-0a26e42ebfbbf75aa', 'vol-0e8de4fa896ed7755', 'vol-0bca1c2d96081e5a3', 'vol-0cb54d2674ef5d685', 'vol-0b5bca47086c6f17a', 'vol-0a2faeeb1bb88edcb', 'vol-09022f6571fe3428c', 'vol-00947a35acc57aa24', 'vol-095b822cc86bdc6e9', 'vol-0418cd4fe3f0549d2', 'vol-01dab10828996c42d', 'vol-070645bd1301fb6bd', 'vol-0feaee0eec87a7ad6', 'vol-0a64de38bc507f353', 'vol-064751e6f8a31523a', 'vol-06850f06768d048e6', 'vol-0b03068401a6c3d20', 'vol-0768bbe8301290412', 'vol-0c4d2f2aa65b5edc6', 'vol-08b79cf2ae3df8de6', 'vol-0421c31a71598b777', 'vol-03fa70e6fb659a8ed', 'vol-0f6d7d123f8ba0c1b', 'vol-001b5525c262e41e0', 'vol-08d29f5a0148beb74', 'vol-04c8c7376d4d2fcb5', 'vol-0461b01ec1ddaa84d', 'vol-0248e372c968f2fc3', 'vol-04a19aeafb43ea76c', 'vol-05fd4a990ce362b79', 'vol-001c52f09a5199f49', 'vol-0212b782259c2573b', 'vol-00f04e5f29a7f0311', 'vol-0e93a88ec3742bb8a', 'vol-04a995f3d7fe096ff', 'vol-04c47218621ef8c62', 'vol-0a97cacd1b02fae5e', 'vol-09fc5e54b176e4d5a', 'vol-0951afb5b8978deee', 'vol-080f23efe0e5cec6f', 'vol-05d34f24e68de0c35', 'vol-0bf6e5b5f060b7dc4', 'vol-0ea3f13ece6f4e6b3', 'vol-0878a46bc5e616641', 'vol-0c08fb6f628251379', 'vol-0e8940f5021bd0621', 'vol-0ff6e1e222a7dff88', 'vol-0615124acdf7e4975', 'vol-07441da4665c421c6', 'vol-0f85963b5ca027242', 'vol-0d25a5f5a1aaca3f9', 'vol-0e13d3e5000503ff0', 'vol-096ec21607e14c653', 'vol-084e8c59c8597b20b', 'vol-05e0d6ce8440ee0c7', 'vol-0aee34107faee78e5', 'vol-05a2ba2b91b3d74f6', 'vol-07b7b2abefcc4c7bd', 'vol-04e1d48ba93e9c6ea', 'vol-0561c5d9a352dd301', 'vol-00b764c6e27d0186e', 'vol-08f17b9bb792a02a6', 'vol-00afad6ffa743ba3b', 'vol-0db852c452756bff7', 'vol-0579dc457da4f491d', 'vol-0e296d39a64b30fe1', 'vol-00efbcdba4624e738', 'vol-0d9cdd6b283298396', 'vol-0218fb58e394f9a72', 'vol-01d9b9f2512e770ec', 'vol-0ebfc2872aa8e41ed', 'vol-04f31b5d70bd8d5db', 'vol-0139dd23c0f02912d', 'vol-027a73e38208e76db', 'vol-0357f331d5d83b200', 'vol-02ca802ac06227930', 'vol-02030678b9f8142fd', 'vol-06d2444cdeeadfe94', 'vol-08c29e1de29294fc6', 'vol-03073c5bf12020e9b', 'vol-099d437bacc325c32', 'vol-08f293d91bc00745b', 'vol-0e5ff463b4f414878', 'vol-07f4f5807513671c3', 'vol-07d5cdc3bff6a4c01', 'vol-04511f65e61f870c4', 'vol-01e04db7b1a4824b9', 'vol-062c71ef3d8a9f758', 'vol-05271a943afd8219f', 'vol-0b119bc044c502c32', 'vol-02daa382e18eee2e7', 'vol-03e49faf15dc0f51d', 'vol-093d5d80b6b3d62a1', 'vol-06bc7f5d52404c2f2', 'vol-05cb615b4b8e844a1', 'vol-0342ea15cb81492e8', 'vol-00e94794fbb9171f7', 'vol-0b9f04992b289e8af', 'vol-084cbdb96e50c0c5a', 'vol-068d203a59d03dad4', 'vol-0770aa418d0607011', 'vol-0212ca60c425d31c4', 'vol-0c4ee6ab1fc97ece5', 'vol-0c8800f4540626f6b', 'vol-0b962ec8ba53dc39d', 'vol-09c9c0f3ce8b9e9cd', 'vol-06a72b2e02ce88223', 'vol-0908201887b315dfd', 'vol-040906ee32c6651c1', 'vol-0d6115b8e1c9a67d6', 'vol-08e08429f6842c7f4', 'vol-0780fda91d3b66427', 'vol-019cadeb34540779f', 'vol-0f11cd76177fa01d8', 'vol-08cd4d4d7794a2d69', 'vol-05ce7d8f7b5465423', 'vol-0c5a5f9a5bb250994', 'vol-0aa11b97bb3b45f00', 'vol-016c04197de9aaa3b', 'vol-0504c5c93a2c6f012', 'vol-0092fad69fd676a8d', 'vol-0ad8c999d76351217', 'vol-03b7b682a86c4c570', 'vol-00815584f6e34d5b3', 'vol-0399f01aad83c9560', 'vol-080488ffcdc3c59fd', 'vol-0a4a6d0dccbd7285f', 'vol-07d5fcc363d1659c3', 'vol-08bda9d3cd47f0fe1', 'vol-0be8518f00aed5088', 'vol-0fcc73fa330ed6376', 'vol-0d9d892c40c275b93', 'vol-096e3d28079bb0d82', 'vol-0416c9223118efe1c', 'vol-0fbdf6d688d96b09c', 'vol-05062bdf93f365780', 'vol-049416795de82c9a0', 'vol-0c8b852c5bc308dbd', 'vol-0d6ff89ef8fb567cc', 'vol-056e674935390bc46', 'vol-0fff35451b871f501', 'vol-030066331c07f55d0', 'vol-0cc16780c5e6222fc', 'vol-02768edd2630a5a44', 'vol-0adb7419cec661b0e', 'vol-016c52ff6d427484c', 'vol-0f18ca708b619545e', 'vol-0d54528806e9d3842', 'vol-024200240c549ce68', 'vol-0ed410c3ce3124ad2']

def copy_snap(response,id,Des):
    # print(response)
    try:
            for k in  range(len(response['Snapshots'][0]['Tags'])):
                    list_tags[response['Snapshots'][0]['Tags'][k]['Key']] = response['Snapshots'][0]['Tags'][k]['Value']
            if 'Name' in list_tags:
                response2 = snap.copy_snapshot(
                       TagSpecifications=[
                                 {
                                    'ResourceType': 'snapshot',
                                    'Tags': [
                                        {
                                            'Key': "Name",
                                            'Value': list_tags["Name"]
                                        },
                                    ]
                                },
                            ],
                        SourceSnapshotId=id,
                        Description=Des,
                        SourceRegion='us-east-1',
                        DestinationRegion='us-east-1',
                        Encrypted=True  
                   )
                print(response2)   
                print(id+" Done")   
                # delete_snap(id)   
            else: 
                response2 = snap.copy_snapshot(
                        SourceSnapshotId=id,
                        Description=Des,
                        DestinationRegion='us-east-1',
                        SourceRegion='us-east-1',
                        Encrypted=True   
                   )
                print(response2)   
                print(id+" Done")   
                # delete_snap(id)
                            
    except:        
              response2 = snap.copy_snapshot(
                        SourceSnapshotId=id,
                        Description=Des,
                        DestinationRegion='us-east-1',
                        SourceRegion='us-east-1',
                        Encrypted=True   
                   )
            #   delete_snap(id)
              print(response2)            
              print(id+" Done")   
                 


# def delete_snap(id):
#     try:
#       response3 = snap.delete_snapshot(
#           SnapshotId=id
#       )
#     except:
#          print("Cant deleted")



with open('volumwmanagemenr/snapupdate/snapdata.yml') as f:
  data = yaml.load(f, Loader=SafeLoader)
  for i in data['snap_id']:
      try:    
        response = snap.describe_snapshots(
            SnapshotIds=[i]
            
        )
        for j in listofvolume:
             if response['Snapshots'][0]['VolumeId'] == j:
                print(response['Snapshots'][0]['VolumeId']) 
                copy_snap(response,i,response['Snapshots'][0]['Description'])
                # delete_snap(i)
      except:
          pass