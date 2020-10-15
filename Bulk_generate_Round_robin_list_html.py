# -*- coding: utf-8 -*-
# v1.2.0
# KR JP CN (And image) with show hide element class support
import itertools
import os
import csv

"""
list1 = ['f', 'o', 'o']
list2 = ['hello', 'world','yeah','man','a','b','c']

print ([x for x in itertools.chain.from_iterable(itertools.zip_longest(list1,list2)) if x])
"""

# CONFIG
#csvLocation = ""+os.path.dirname(__file__) + "\\Bulk_Generate_KrJp_def\\" + "KRDict_JP_All_Full_edited.csv"

csvLocation = ""+os.path.dirname(__file__) + "\\list7.csv"

# (use element_text output if planning to use HTML_Splitter.py directly without using calibre) #
plain_text_or_element_text_output = "element_text"    # i.e. plain_text ==「わ、わかりませんっ」,   element_text ==<p class="calibre1">「わ、わかりませんっ」 </p>   .


# END CONFIG
def csvToRoundrobinList(fileName):
    L1 = []
    L2 = []
    L3 = []
    L4 = []
    with open(fileName, "r", encoding="utf-8")as tsvfile:
        reader = csv.DictReader(tsvfile,delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            L1.append([row["KR"],"KR"])
            L2.append([row["JP"],"JP"])
            if "CN" in row:
                L3.append([row["CN"],"CN"])
            if "IMAGE" in row:
                L4.append([row["IMAGE"],"IMAGE"])   # Only needs file name + extension. No Quote needed  I.e. kuchie-001.jpg .

        L4 = [['<img class="fit" src="image/%s" alt="" />' %x[0], x[1]] if x[0] else x for x in L4]  # convert image rows into something like <img class="fit" src="image/kuchie-001.jpg" alt="" />

    finalL = makeRoundRobinList(L1,L2,L3,L4)


    #now make file
    with open('Hikaru v1 KR JP CN.txt', 'w', encoding="utf-8") as f:
        """
        for item in finalL:
            if plain_text_or_element_text_output == 'element_text':
                f.write('<p class="calibre1">%s </p>\n' % item)
            elif plain_text_or_element_text_output == 'plain_text':
                f.write('%s\n' % item)"""
        for item in finalL:
            #print(item)
            if plain_text_or_element_text_output == 'element_text':
                f.write('<p class="calibre1 %s">%s </p>\n' % (item[1], item[0]))
            elif plain_text_or_element_text_output == 'plain_text':
                f.write('%s\n' % item[0])


def makeRoundRobinList(L1,L2,L3=None,L4=None):
    if not L3:
        # if L3 is None then create blank placeholder
        L3 = [[None,"None"] for x in L1]
    if not L4:
        # if L4 is None then create blank placeholder
        L4 = [[None,"None"] for x in L1]

    return ([x for x in itertools.chain.from_iterable(itertools.zip_longest(L1,L2,L3,L4)) if x[0]])



csvToRoundrobinList(csvLocation)

print("Check out KR JP Lines Template.xlsx ! ")
