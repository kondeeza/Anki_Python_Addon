# -*- coding: utf-8 -*-
'''
Created on 09/12/2014

@author: Myxoma
'''
import sqlite3
import os

db = sqlite3.connect('B:\mydb.sqlite')

print((__file__))
print(os.path.dirname(__file__))

x = ""+os.path.dirname(__file__) + "\DB_FOLDER"
print(x)

#

# Begin Manual Config
FrequencyDBSubfolderName = "\DB_FOLDER"
FrequencyDBname = "frequency.db"
#End manual Config

FrequencyDBFullPath = ""+os.path.dirname(__file__) + FrequencyDBSubfolderName + FrequencyDBname
print(FrequencyDBFullPath)

