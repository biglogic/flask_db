
from json2html import *
import  sys



#Modify this to fit your need

n = len(sys.argv)

# print("Total arguments passed:", n)
sys.argv[1]
file = open(sys.argv[1], "r")

data = file.read()
test = json2html.convert(json = data)
print(test)