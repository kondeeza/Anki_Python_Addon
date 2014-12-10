# -*- coding: utf-8 -*-
'''
Created on 08/12/2014

@author: Myxoma
'''
"""
#y = ["hello","bomb*","pizza","aha^","rubic"]
x = []

for i in y:
    
    if (i.find("*") !=-1 or i.find("^") !=-1 ):
        x.append(i)
        

for i in y:
    if (i.find("*") ==-1 and i.find("^") ==-1 ):
        x.append(i)
        

"""


input ="内乱^<br />反乱<br />乱す*^<br />乱れる*^<br />反乱<br />乱暴*^<br />"

y = input.split("<br />")
"""
x = []


for i in y:
    if (i.find("*") !=-1 or i.find("^") !=-1 ):
        x.append(i + "<br />")
        
for i in y:
    if (i.find("*") ==-1 and i.find("^") ==-1 and i !=""):
        x.append(i + "<br />")
for i in x:
    print i
    
str1 = "".join(x)
print str1
"""


def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set( x for x in seq if x in seen or seen_add(x) )
    # turn the set into a list (as requested)
    return list( seen_twice )

def listToString(input):
    str1 = "".join(input)
    return str1

x =[]
for i in y:
    x.append(i + "<br />")

x.pop()


x = list_duplicates(x)
x = listToString(x)
print x
