import argparse
import boto3 , datetime
from botocore.exceptions import ClientError
from dateutil.parser import parse

session = boto3.Session(profile_name="atul")
iam_client = session.client('iam')
# parser = argparse.ArgumentParser()
# parser.add_argument("-u", "--username", help="An IAM username, e.g. key_rotator.py --username <username>")
# parser.add_argument("-k", "--key", help="An AWS access key, e.g. key_rotator.py --key <access_key>")
# parser.add_argument("--disable", help="Disables an access key", action="store_true")
# parser.add_argument("--delete", help="Deletes an access key", action="store_true")
# args = parser.parse_args()
# username = args.username
# aws_access_key = args.key
age_day = []

def get_keys(user_name):
   access_key = iam_client.list_access_keys(UserName=user_name)
   for i in access_key["AccessKeyMetadata"]:
      print(i["CreateDate"]) 
      days_old(str(i["CreateDate"]),access_key["AccessKeyMetadata"][0]["AccessKeyId"],user_name) 
  
def days_old(date,access_key_id,username):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    print(date_obj)
    diff = datetime.datetime.now() - date_obj
    if diff.days > 200:
        create_key("atulhaha")
    if diff.days > 170:
        delete_key(access_key_id,username)


def create_key(username):
        print("%s already has 2 keys. You must delete a key before you can create another key." % (username))
        access_key_metadata=iam_client.create_access_key(UserName=username)['AccessKey']
        access_key = access_key_metadata['AccessKeyId']
        secret_key = access_key_metadata['SecretAccessKey']
        print("your new access key is %s and your new secret key is %s" % (access_key, secret_key))

# def disable_key(access_key, username):


def delete_key(access_key, username):
    try:
            iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
            print (access_key + " has been deleted.")
    except ClientError as e:
        print ("The access key with id %s cannot be found" % access_key)


get_keys("atulhaha")