# -*- coding: utf-8 -*-
import itertools
import os
import csv
import re
"""
list1 = ['f', 'o', 'o']
list2 = ['hello', 'world','yeah','man','a','b','c']

print ([x for x in itertools.chain.from_iterable(itertools.zip_longest(list1,list2)) if x])
"""
debugmode = True
out_f = open('outputfile.txt', 'w', encoding="utf-8")

with open('file.txt', mode="r", encoding="utf-8") as f:
    str = '"This" is my "new" key "string"';
    str = re.sub('"([^"]*)"', '{$1}', 'hello number 10, Agosto 19')

    """ 
    The "([^"]*)" regex captures a ", followed by 0 or more things that aren't another ", and a closing ". 
    The replacement uses $1 as a reference for the things that were wrapped in quotes.
    see https://stackoverflow.com/questions/53901717/string-replace-double-quotes-into-curly-brackets
    """
    incomplete_quote = False
    incomplete_quote2 = False
    incomplete_quote3 = False
    incomplete_quote4 = False
    for line in f:
        if line not in ['\n', '\r\n']:  # if line not empty
            #print(line.strip())
            if '「' in line and not '」' in line and incomplete_quote is False:
               incomplete_quote = True
            if '『' in line and not '』' in line and incomplete_quote2 is False:
                incomplete_quote2 = True
            if '（' in line and not '）' in line and incomplete_quote3 is False:
                incomplete_quote3 = True
            if '“' in line and not '”' in line and incomplete_quote4 is False:
                incomplete_quote4 = True
            out_f.write('%s' % line.strip())

            if incomplete_quote is False and incomplete_quote2 is False and incomplete_quote3 is False and incomplete_quote4 is False:
                if line.strip()[-1] in ['.', '◇', '」', '』', '?', '!!', '!', '）', '”']:
                    out_f.write('\n')
            if incomplete_quote is True:
                if line.strip()[-1] in ['」']:
                    out_f.write('\n')
                    incomplete_quote = False
            if incomplete_quote2 is True:
                if line.strip()[-1] in ['』']:
                    out_f.write('\n')
                    incomplete_quote2 = False
            if incomplete_quote3 is True:
                if line.strip()[-1] in ['）']:
                    out_f.write('\n')
                    incomplete_quote3 = False
            if incomplete_quote4 is True:
                if line.strip()[-1] in ['”']:
                    out_f.write('\n')
                    incomplete_quote4 = False

            if debugmode:
                print("incomplete_qte:%i incomplete_qte2:%i incomplete_qte3:%i incomplete_qte4:%i line[-1] in[. ◇ 」 』 ? !! ! )”]:%i line[-1] contains 」:%i txt: %s" % (incomplete_quote, incomplete_quote2,incomplete_quote3,incomplete_quote4, line.strip()[-1] in ['.', '◇', '」', '』', '?', '!!', '!', '）', '”'],line.strip()[-1] in ['」'],line.strip() ))





csvLocation = ""+os.path.dirname(__file__) + "\\list2.csv"
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
    with open('SSS Class Suicide Hunter_KR_JP_1-50.txt', 'w', encoding="utf-8") as f:
        for item in finalL:
            #f.write('<p class="calibre1">%s </p>\n' % item)
            f.write('%s\n' % item)


def makeRoundRobinList(L1,L2):
    return ([x for x in itertools.chain.from_iterable(itertools.zip_longest(L1,L2)) if x])


"""
csvToRoundrobinList(csvLocation)

"""
