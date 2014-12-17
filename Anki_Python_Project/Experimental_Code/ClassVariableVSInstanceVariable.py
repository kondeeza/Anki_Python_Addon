'''
Created on 16/12/2014

@author: Myxoma
'''

class Test(object):
    i = 3
    
    
print Test.i

t = Test()
print t.i     # static variable accessed via instancet.i = 5 # but if we assign to the instance ...
t.i = 5 # but if we assign to the instance ...
print Test.i  # we have not changed the static variable
print t.i     # we have overwritten Test.i on t by creating a new attribute t.iTest.i = 6 # to change the static variable we do it by assigning to the classt.iTest.i
Test.i = 6 # to change the static variable we do it by assigning to the class
print t.i
print Test.i
u = Test()
print u.i # changes to t do not affect new instances of Test

# Namespaces are one honking great idea -- let's do more of those!
print Test.__dict__
print t.__dict__
print u.__dict__

"""
Notice how the instance variable t.i got out of sync with the "static" class variable when the attribute i was set directly on t.
 This is because i was re-bound within the t namespace
,which is distinct from the Test namespace. If you want to change the value of a "static" variable, 
you must change it within the scope (or object) where it was originally defined.
 I put "static" in quotes because Python does not really have static variables in the sense that C++ and Java do.
"""
