# -*- coding: utf-8 -*-
import itertools
import os
import csv
import re
import xml.etree.ElementTree as ET


debugmode = True
limit = 100000

myENTagDict = {}
x = {}
with os.scandir('Input2/en_US') as entries:
    for mXMLFileToTL in entries:
        # print(mXMLFileToTL.name)

        myCurrent_EN_XML = ET.parse(mXMLFileToTL)

        myENTagList = {elem for elem in myCurrent_EN_XML.iter('Row') if elem.attrib['Tag'] }

        # print(len(myENTagList))

        for index, item in enumerate(myENTagList):
            myENTagDict[item.attrib['Tag']] = item[0].text

# print (len(myENTagDict))  #14885
# print (myENTagDict['LOC_AUSTRALIA_MOD_TITLE']) #DLC: Australia Civilization Pack


# parse an xml file by name
my_KR_XML = ET.parse('Input2/Vanilla_ko_KR.xml')


myKRTagList = {elem for elem in my_KR_XML.iter('Replace')}


for index, item in enumerate(myKRTagList):
    """
    print(item.attrib['Tag'])
    print(item[0].text)
    """
    if item.attrib['Tag'] in myENTagDict and item[0].text and myENTagDict.get(item.attrib['Tag']):
        # print(JPDict.get(item.attrib['Tag']))
        item[0].text = item[0].text + " " + myENTagDict.get(item.attrib['Tag'])

    # item[0].text = item[0].text + "LOL"
    if index == limit: # There's gotta be a better way.
        break

my_KR_XML.write('Output2/Vanilla_ko_KR.xml', encoding="UTF-8",xml_declaration=True)
