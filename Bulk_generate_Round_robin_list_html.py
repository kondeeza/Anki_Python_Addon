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

inputname = "list.csv"
outputname = "The Second Coming_Dual Sub 101-200.html"
csvLocation = ""+os.path.dirname(__file__) + "\\" + inputname

"Kobo_Span"
"Formatted_HTML"
"Raw_Text"
outputformat = "Formatted_HTML"
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
    with open( outputname, 'w', encoding="utf-8") as f:

        if outputformat == "Formatted_HTML":
            f.write("""<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>""" + outputname + """</title><link href="HontoHtmlOutBasicCss.css" type="text/css" rel="stylesheet" /></head><body>""")

        for item in finalL:
            if outputformat == "Kobo_Span":
                f.write('<p class="calibre"><span class="kobospan"> %s </span></p>\n' % item)
            elif outputformat == "Formatted_HTML":
                f.write('<p class="calibre">%s </p>\n' % item)
            elif outputformat == "Raw_Text":
                f.write('%s\n' % item)

        if outputformat == "Formatted_HTML":
            f.write("< / body > < / html >")
def makeRoundRobinList(L1,L2):
    return ([x for x in itertools.chain.from_iterable(itertools.zip_longest(L1,L2)) if x])



csvToRoundrobinList(csvLocation)

