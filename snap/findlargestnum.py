
listofnum = [23,45,22,54,32,66]
list2 = []
x = "ho"

def get_largest ():
    for i in listofnum:
        x = i 
        for j in listofnum:
            if j > x :
               x = j
    print(x)


get_largest()