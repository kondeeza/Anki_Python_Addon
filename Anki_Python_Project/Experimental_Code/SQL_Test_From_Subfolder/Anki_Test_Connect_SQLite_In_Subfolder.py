# -*- coding: utf-8 -*-
'''
Created on 09/12/2014

@author: Myxoma
'''
import sqlite3
import os

#db = sqlite3.connect('B:\mydb.sqlite')

# Begin Manual Config
FrequencyDBSubfolderName = "\DB_FOLDER\\"
FrequencyDBname = "freq.sqlite"
#End manual Config

FrequencyDBLocation = ""+os.path.dirname(__file__) + FrequencyDBSubfolderName + FrequencyDBname
#print(FrequencyDBLocation)

FQdb = sqlite3.connect(FrequencyDBLocation)

vocabToQuery = "相当"
mQuery = "select freq from Dict where expression =\"" + vocabToQuery + "\";"
print mQuery

cursor = FQdb.cursor()
cursor.execute(mQuery)
FQResult_Single = cursor.fetchone() #retrieve the first row
print(FQResult_Single[0]) #Print the first column retrieved

"""
all_rows = cursor.fetchall()
for row in all_rows:
    # row[0] returns the first column in the query (name), row[1] returns email column.
    print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
"""