# -*- coding: utf-8 -*-
import itertools
import os
import csv
import re
import xml.etree.ElementTree as ET


debugmode = True
limit = 100000

# parse an xml file by name
myKRdoc = ET.parse('Vanilla_ko_KR.xml')
myJPdoc = ET.parse('Vanilla_ja_JP.xml')


myJPTagList = {elem for elem in myJPdoc.iter('Replace')}
myKRTagList = {elem for elem in myKRdoc.iter('Replace')}

JPDict = {}

for index, item in enumerate(myJPTagList):
    JPDict[item.attrib['Tag']] = item[0].text

# print(len(JPDict))

for index, item in enumerate(myKRTagList):
    """
    print(item.attrib['Tag'])
    print(item[0].text)
    """
    if item.attrib['Tag'] in JPDict and item[0].text and JPDict.get(item.attrib['Tag']):
        # print(JPDict.get(item.attrib['Tag']))
        item[0].text = item[0].text + " " + JPDict.get(item.attrib['Tag'])

    # item[0].text = item[0].text + "LOL"
    if index == limit: # There's gotta be a better way.
        break

myKRdoc.write('file_new.xml', encoding="UTF-8",xml_declaration=True)
