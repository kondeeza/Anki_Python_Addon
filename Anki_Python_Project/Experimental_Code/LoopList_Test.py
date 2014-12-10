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


input ="内乱^<br />反乱<br />乱す*^<br />乱れる*^<br />混乱<br />乱暴*^<br />"

y = input.split("<br />")
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