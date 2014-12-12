# -*- coding: utf-8 -*-
'''
Created on 09/12/2014

@author: Myxoma
'''
import sqlite3
import os

#db = sqlite3.connect('B:\mydb.sqlite')

# Begin Manual Config
DictDBSubfolderName = "\DB_FOLDER\\"
DictDBname = "dict.sqlite"
#End manual Config

FrequencyDBLocation = ""+os.path.dirname(__file__) + DictDBSubfolderName + DictDBname
#print(FrequencyDBLocation)

DictDBname = sqlite3.connect(FrequencyDBLocation)

#vocabToQuery = "雨子"
vocabToQuery = "明白"
if (vocabToQuery != ""):
    mQuery = "select kana from Dict where kanji =\"" + vocabToQuery + "\";"
    cursor = DictDBname.cursor()
    cursor.execute(mQuery)
    FQResult_AllRows = cursor.fetchall() #retrieve all row
    if (FQResult_AllRows != None):
        if (len(FQResult_AllRows) ==1):
            #append1 1 {Kana}
            print ("is @1")
        elif (len(FQResult_AllRows) ==2 and (FQResult_AllRows[0] == FQResult_AllRows[1])):
            #append 2E, 1{Kana}
            print ("is @2E, 2 result but result equal")
        elif (len(FQResult_AllRows) ==2):
            #append 2, 2 {Kana}
            print ("is @2, 2 result")
        elif (len(FQResult_AllRows) >=3):
            #append 3, first 3 {Kana}
            print ("is @3, 3 result or more")
        #print(FQResult_AllRows[0]) #Print the first column retrieved
        #print (len(FQResult_AllRows))
        #print (len(FQResult_AllRows[0]))

    for row in FQResult_AllRows:
        print(row[0])
"""
all_rows = cursor.fetchall()
for row in all_rows:
    # row[0] returns the first column in the query (name), row[1] returns email column.
    print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
"""