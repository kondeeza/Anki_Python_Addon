# -*- coding: utf-8 -*-
import itertools
import os
import csv
import re
import xml.etree.ElementTree as ET


debugmode = True
limit = 100000

# parse an xml file by name

with os.scandir('Input/') as entries:
    for mXMLFileToTL in entries:
        # print(mXMLFileToTL.name)

        myCurrentXML = ET.parse(mXMLFileToTL)


        # myJPTagList = {elem for elem in myJPdoc.iter('Replace')}
        myKRTagList = {elem for elem in myCurrentXML.iter('Replace') if elem.attrib['Language'] =='ko_KR' }
        myJPTagList = {elem for elem in myCurrentXML.iter('Replace') if elem.attrib['Language'] =='ja_JP' }

        print (len(myKRTagList))
        print (len(myJPTagList))
        JPDict = {}

        for index, item in enumerate(myJPTagList):
            JPDict[item.attrib['Tag']] = item[0].text



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

        myCurrentXML.write('Output/'+ mXMLFileToTL.name, encoding="UTF-8", xml_declaration=True)


