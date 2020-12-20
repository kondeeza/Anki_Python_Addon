import os
import xml.etree.ElementTree as ET

tree = ET.parse('kanjidic2.xml')
root = tree.getroot()

i = 1
KanjiList_XML = root.findall('character')
print (KanjiList_XML[0][0].text)

for Kanji in KanjiList_XML:
    if i <=100:
        literal = Kanji.find('literal').text
        strokecount = Kanji.find('misc').find('stroke_count').text
        #unicodeNumber
        #JouyouGrade
        #Frequency
        #Onyomi
        #Kunyomi
        #Meaning
        #HeisigNumber
        print(literal,strokecount, Kanji.getparent())

        i += 1
    else:
        break
print("finished2")