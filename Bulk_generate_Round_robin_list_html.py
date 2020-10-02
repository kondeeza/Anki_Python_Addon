# -*- coding: utf-8 -*-
import itertools
import os
import csv
"""
list1 = ['f', 'o', 'o']
list2 = ['hello', 'world','yeah','man','a','b','c']

print ([x for x in itertools.chain.from_iterable(itertools.zip_longest(list1,list2)) if x])
"""

#csvLocation = ""+os.path.dirname(__file__) + "\\Bulk_Generate_KrJp_def\\" + "KRDict_JP_All_Full_edited.csv"

csvLocation = ""+os.path.dirname(__file__) + "\\list4.csv"
def csvToRoundrobinList(fileName):
    L1 = []
    L2 = []
    with open(fileName, "r", encoding="utf-8")as tsvfile:
        reader = csv.DictReader(tsvfile,delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            L1.append(row["KR"])
            L2.append(row["JP"])
    finalL = makeRoundRobinList(L1,L2)


    #now make file
    with open('Torture Princess Vol1 KR JP.txt', 'w', encoding="utf-8") as f:
        for item in finalL:
            #f.write('<p class="calibre1">%s </p>\n' % item)
            f.write('%s\n' % item)


def makeRoundRobinList(L1,L2):
    return ([x for x in itertools.chain.from_iterable(itertools.zip_longest(L1,L2)) if x])



csvToRoundrobinList(csvLocation)

