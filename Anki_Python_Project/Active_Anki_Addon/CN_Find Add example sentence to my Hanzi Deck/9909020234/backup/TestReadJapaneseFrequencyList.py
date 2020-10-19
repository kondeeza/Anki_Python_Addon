import os
import xml.etree.ElementTree as ET

tree = ET.parse('kanjidic2.xml')
root = tree.getroot()

i = 1
for elem in tree.iter(tag='character'):
    if i <=100:
        print(elem.tag, [childE.tag for childE in elem])
        i += 1
    else:
        break

print("finished")