# -*- coding: utf-8 -*-
'''
Created on 13/12/2014

@author: Myxoma
'''
import re
import sqlite3
import os

# Begin Manual Config
DictDBSubfolderName = "\DB_FOLDER\\"
DictDBname = "dict.sqlite"
#End manual Config

FrequencyDBLocation = ""+os.path.dirname(__file__) + DictDBSubfolderName + DictDBname
#print(FrequencyDBLocation)

Dictdb = sqlite3.connect(FrequencyDBLocation)

# showInfo ("--> Everything should have worked. Trying Regex")
TextOutput = "お先に(おさきに): before, ahead, previously<br />先に(さきに): before, earlier than, ahead, beyond, away, previously, recently<br />先行(せんこう): preceding, going first<br />先代(せんだい): family predecessor, previous age, previous generation<br />先だって(せんだって): recently, the other day<br />先着(せんちゃく): first arrival<br />先天的(せんてんてき): a priori, inborn, innate, inherent, congenital, hereditary<br />勤め先(つとめさき): place of work<br />優先(ゆうせん): preference, priority<br />先程(さきほど): some time ago<br />先日(せんじつ): the other day, a few days ago<br />先々月(せんせんげつ): month before last<br />先々週(せんせんしゅう): week before last<br />先祖(せんぞ): ancestor<br />先端(せんたん): pointed end, tip, fine point, spearhead, cusp, vanguard, advanced, leading edge<br />先頭(せんとう): head, lead, vanguard, first<br />祖先(そせん): ancestor<br />先ず(まず): at first<br />真っ先(まっさき): the head, the foremost, beginning<br />先輩(せんぱい): one's senior<br />先(さき): the future, forward, priority, precedence, former, previous, old, late<br />先月(せんげつ): last month<br />先週(せんしゅう): last week, the week before<br />先生(せんせい): teacher, master, doctor"

TextOutput = "義理(ぎり): duty, sense of duty, honor, decency, courtesy, debt of gratitude, social obligation<br />真理(しんり): truth<br />推理(すいり): reasoning, inference, mystery or detective genre (movie novel etc.)<br />生理(せいり): physiology, menses<br />調理(ちょうり): cooking<br />理屈(りくつ): theory, reason<br />理性(りせい): reason, sense<br />理論(りろん): theory<br />論理(ろんり): logic<br />管理(かんり): control, management (e.g. of a business)<br />原理(げんり): principle, theory, fundamental truth<br />合理(ごうり): rational<br />修理(しゅうり): repairing, mending<br />処理(しょり): processing, dealing with, treatment, disposition, disposal<br />心理(しんり): mentality<br />整理(せいり): sorting, arrangement, adjustment, regulation<br />総理大臣(そうりだいじん): Prime Minister<br />代理(だいり): representation, agency, proxy, deputy, agent, attorney, substitute, alternate, acting (principal, etc.)<br />物理(ぶつり): physics<br />理科(りか): science<br />理解(りかい): understanding, comprehension<br />理想(りそう): ideal<br />地理(ちり): geography, geographical features<br />無理(むり): compulsion<br />理由(りゆう): reason<br />料理(りょうり): cooking, cookery, cuisine"
TextOutput = "貫禄(かんろく): presence, dignity<br />貫く(つらぬく): to go through"
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
x = []

"""
for i in y:
    print (i)
print

for i in KanaReading:
    print (i)
"""
"""
i = 0
while i < len(y):
    print (y[i] +" : " + KanaReading[i])
    i+=1
    """

i = 0
while i < len(y):
    vocabToQuery = y[i]
    if (vocabToQuery != ""):
        mQuery = "select kana from Dict where kanji =\"" + vocabToQuery + "\";"
        cursor = Dictdb.cursor()
        cursor.execute(mQuery)
        Result_AllRows = cursor.fetchall() #retrieve all row
        if (Result_AllRows != None):
            if (len(Result_AllRows) ==1):
                #append1 1 {Kana}
                #print ("is @1")
                if (Result_AllRows[0][0] == KanaReading[i].decode('utf-8')):
                    x.append("@1, " + y[i].decode('utf-8') +" (" + KanaReading[i].decode('utf-8') +"): " + Result_AllRows[0][0] + "<br />")
                    #just do nothing e.g. do lol = 2
                    lol = 2
                else:
                    x.append("@1NotEqual, " + y[i].decode('utf-8') +" (" + KanaReading[i].decode('utf-8') +"): " + Result_AllRows[0][0] + "<br />")
            elif (len(Result_AllRows) ==2 and (Result_AllRows[0][0] == Result_AllRows[1][0])):
                #append 2E, 1{Kana}
                #print ("is @2E, 2 result but result equal")
                x.append("@2E, " + y[i].decode('utf-8') +" (" + KanaReading[i].decode('utf-8') +"): " +  Result_AllRows[0][0] + "<br />")
            elif (len(Result_AllRows) ==2):
                #append 2, 2 {Kana}
                #print ("is @2, 2 result")
                x.append("@2, " +  y[i].decode('utf-8') +" (" + KanaReading[i].decode('utf-8') +"): " + Result_AllRows[0][0] +", " + Result_AllRows[1][0] + "<br />")
            elif (len(Result_AllRows) >=3):
                #append 3, first 3 {Kana}
                #print ("is @3, 3 result or more")
                x.append("@2, " +  y[i].decode('utf-8') +" (" + KanaReading[i].decode('utf-8') +"): " + Result_AllRows[0][0] +", " + Result_AllRows[1][0] + ", " + Result_AllRows[2][0] + "<br />")
    i+=1
    
for i in x:
    print (i)
answer = "".join(x)

