# -*- coding: utf-8 -*-
'''
Created on 13/12/2014

@author: Myxoma
'''
import re


# showInfo ("--> Everything should have worked. Trying Regex")
TextOutput = "お先に(おさきに): before, ahead, previously<br />先に(さきに): before, earlier than, ahead, beyond, away, previously, recently<br />先行(せんこう): preceding, going first<br />先代(せんだい): family predecessor, previous age, previous generation<br />先だって(せんだって): recently, the other day<br />先着(せんちゃく): first arrival<br />先天的(せんてんてき): a priori, inborn, innate, inherent, congenital, hereditary<br />勤め先(つとめさき): place of work<br />優先(ゆうせん): preference, priority<br />先程(さきほど): some time ago<br />先日(せんじつ): the other day, a few days ago<br />先々月(せんせんげつ): month before last<br />先々週(せんせんしゅう): week before last<br />先祖(せんぞ): ancestor<br />先端(せんたん): pointed end, tip, fine point, spearhead, cusp, vanguard, advanced, leading edge<br />先頭(せんとう): head, lead, vanguard, first<br />祖先(そせん): ancestor<br />先ず(まず): at first<br />真っ先(まっさき): the head, the foremost, beginning<br />先輩(せんぱい): one's senior<br />先(さき): the future, forward, priority, precedence, former, previous, old, late<br />先月(せんげつ): last month<br />先週(せんしゅう): last week, the week before<br />先生(せんせい): teacher, master, doctor"

KanaReading = TextOutput
#showInfo(TextOutput)

""" Ensure All <br> format considered"""
TextOutput = re.sub('\((.*?)\)[:](.*?)(<br />)', "<br />", TextOutput)
#showInfo(TextOutput)
TextOutput = re.sub('\((.*?)\)[:](.*?)(<br/>)', "<br />", TextOutput)
#showInfo(TextOutput)
TextOutput = re.sub('\((.*?)\)[:](.*?)(<br>)', "<br />", TextOutput)
#showInfo(TextOutput)
TextOutput = re.sub('\((.*?)\)[:](.*)', "<br />", TextOutput)
#showInfo(TextOutput)
y = TextOutput.split("<br />")
KanaReading = re.sub(r'.*?\((.*?)\)[:].*?(<br />)', r"(\1)\2", KanaReading)
KanaReading = re.sub(r'.*?\((.*?)\)[:].*?(<br/>)', r"(\1)\2", KanaReading)
KanaReading = re.sub(r'.*?\((.*?)\)[:].*?(<br>)', r"(\1)\2", KanaReading)
KanaReading = re.sub(r'<br />[^(].*?\((.*?)\)[:].*', r"<br />\1<br />", KanaReading)
KanaReading = re.sub(r'\((.*?)\).*?(<br />)', r"\1<br />", KanaReading)
KanaReading = KanaReading.split("<br />")

"""
for i in y:
    print (i)
print

for i in KanaReading:
    print (i)
"""
i = 0
while i < len(y):
    print (y[i] +" : " + KanaReading[i])
    i+=1