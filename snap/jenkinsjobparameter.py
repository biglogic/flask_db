from unicodedata import name
from venv import create
import jenkinsapi
import sys
from jenkinsapi.jenkins import Jenkins 



get_url = Jenkins(baseurl='http://44.204.27.229:8080',username="atul",password="aksingh")

list_= get_url.get_jobs_list()

info_ = get_url.get_jobs_info()


for i in info_:
    print(i)

