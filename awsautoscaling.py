import boto3

session = boto3.Session(profile_name="atul" , region_name="us-west-2")
response = session.client("autoscaling")
response2 = response.describe_auto_scaling_groups()
print(response2['AutoScalingGroups'][0]['AutoScalingGroupName']  ,response2['AutoScalingGroups'][0]['MaxSize'] )
response3 = response.update_auto_scaling_group(
    AutoScalingGroupName=response2['AutoScalingGroups'][0]['AutoScalingGroupName'],
    LaunchConfigurationName=response2['AutoScalingGroups'][0]['LaunchConfigurationName'],
    MaxSize=int(response2['AutoScalingGroups'][0]['MaxSize'])+1,
)