# -*- coding: utf-8 -*-
# Copyright: Chris Langewisch <ccl09c@my.fsu.edu>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Based on japanese.reading by Damien Elmes <anki@ichi2.net>
# Bulk copy data in one field to another.


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo
import re
import sqlite3
import os

##########################################################################
# USE LOWERCASE. Model name must contain this.
modelName = 'Heisig'
# each field name must be exact!
Word_SrcField = 'Words'
dstField = 'Words_Clozed'
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
##########################################################################

# Begin Manual Config
DictDBSubfolderName = "\Bulk_Generate_Clozed_RTK_Vocab_Reading_Check\\"
DictDBname = "dict.sqlite"
#End manual Config

def cleanBrFormat(pInput):
     pInput = re.sub(r'(<br>)', r"<br />", pInput)
     pInput = re.sub(r'(<br/>)', r"<br />", pInput)
     pInput = re.sub(r'(<br >)', r"<br />", pInput)
     return pInput
def bulkCheckVocabReadingRTK(nids):
    mw.checkpoint("Bulk-Generate ReIndexed Clozed Vocab Reading Check")
    mw.progress.start()
    
    DictDBLocation = ""+os.path.dirname(__file__) + DictDBSubfolderName + DictDBname    
    Dictdb = sqlite3.connect(DictDBLocation)
    
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
            continue
        src1 = None
        if Word_SrcField in note:
            src1 = Word_SrcField
        if not src1:
            # no src1 field
            showInfo ("--> Field %s not found." % (Word_SrcField))
            continue
        dst = None
        if dstField in note:
            dst = dstField
        if not dst:
            showInfo ("--> Field %s not found!" % (dstField))
            # no dst field
            continue
        if note[dst] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            showInfo ("--> %s not empty. Skipping!" % (Word_SrcField))
            continue
        try:
            # showInfo ("--> Everything should have worked. Trying Regex")
            TextOutput = note[src1]
            KanaReading = TextOutput
            #showInfo(TextOutput)
            KanaReading = cleanBrFormat(KanaReading)
            KanaReading = re.sub(r'.*?\((.*?)\)[:].*?(<br />)', r"(\1)\2", KanaReading)
            #showInfo(KanaReading)
            KanaReading = re.sub(r'.*?\((.*?)\)[:].*?(<br/>)', r"(\1)\2", KanaReading)
            #showInfo(KanaReading)
            KanaReading = re.sub(r'.*?\((.*?)\)[:].*?(<br>)', r"(\1)\2", KanaReading)
            #showInfo(KanaReading)
            KanaReading = re.sub(r'<br />[^(].*?\((.*?)\)[:].*', r"<br />\1<br />", KanaReading)
            #showInfo(KanaReading)
            KanaReading = re.sub(r'\((.*?)\).*?(<br />)', r"\1<br />", KanaReading)
            #showInfo(KanaReading)
            if (KanaReading ==TextOutput):
                #showInfo ("Kana Reading has not been changed after Regex !!!")
                KanaReading = re.sub(r'.*\((.*?)\).*', r"\1<br />", KanaReading)

            KanaReading = KanaReading.split("<br />")
            #showInfo(" @ beforepop KanaReading length: %d" % len(KanaReading))
            
            """
            for i in KanaReading:
                showInfo (" @ beforepop & Aftersplit KanaReading data : %s" % i)"""
            """ Ensure All <br> format considered"""
            TextOutput = cleanBrFormat(TextOutput)
            TextOutput = re.sub('\((.*?)\)[:](.*?)(<br />)', "<br />", TextOutput)
            #showInfo(TextOutput)
            TextOutput = re.sub('\((.*?)\)[:](.*)', "<br />", TextOutput)
            #showInfo(TextOutput)
            y = TextOutput.split("<br />")
            #showInfo(" @ beforepop y length: %d" % len(y))
            #for i in y:
            #    showInfo (" @ beforepop & Aftersplit y data : %s" % i)
            if (len(y) !=0):
                y.pop()


            #showInfo (" @ beforepop & Aftersplit KanaReading length : %s" % len(KanaReading))
            if (len(KanaReading) !=0):
                KanaReading.pop()            
            x = []

            i = 0
            while i < len(y):
                #showInfo ("@ Beginning, i : %d" % i)
                vocabToQuery = y[i]
                #showInfo ("@ Beginning, y length is : %d" % len(y))
                #showInfo ("@ Beginning, Vocab To Query(y[i]) is : %s" % vocabToQuery)
                
                if (vocabToQuery != ""):
                    mQuery = "select kana from Dict where kanji =\"" + vocabToQuery + "\";"
                    cursor = Dictdb.cursor()
                    cursor.execute(mQuery)
                    Result_AllRows = cursor.fetchall() #retrieve all row
                    if (Result_AllRows != None):
                        #showInfo ("@ Middle, Result_AllRows[0][0] is : %s" % Result_AllRows[0][0])
                        #showInfo ("@ Middle, KanaReading[i] is : %s" % KanaReading[i])
                        if (len(Result_AllRows) ==1):
                            #append1 1 {Kana}
                            #print ("is @1") and got list index out of range
                            if (Result_AllRows[0][0] == KanaReading[i]):
                                #x.append("@1, " + y[i] +" (" + KanaReading[i] +"): " + Result_AllRows[0][0] + "<br />")
                                #just do nothing e.g. do lol = 2
                                lol = 2
                            else:
                                x.append("@1NotEqual, " + y[i] +" (" + KanaReading[i] +"): " + Result_AllRows[0][0] + "<br />")
                        elif (len(Result_AllRows) ==2 and (Result_AllRows[0][0] == Result_AllRows[1][0])):
                            #append 2E, 1{Kana}
                            #print ("is @2E, 2 result but result equal")
                            x.append("@2E, " + y[i] +" (" + KanaReading[i] +"): " +  Result_AllRows[0][0] + "<br />")
                        elif (len(Result_AllRows) ==2):
                            #append 2, 2 {Kana}
                            #print ("is @2, 2 result")
                            x.append("@2, " +  y[i] +" (" + KanaReading[i] +"): " + Result_AllRows[0][0] +", " + Result_AllRows[1][0] + "<br />")
                        elif (len(Result_AllRows) >=3):
                            #append 3, first 3 {Kana}
                            #print ("is @3, 3 result or more")
                            x.append("@3, " +  y[i] +" (" + KanaReading[i] +"): " + Result_AllRows[0][0] +", " + Result_AllRows[1][0] + ", " + Result_AllRows[2][0] + "<br />")
                #showInfo ("@ Ending, i : %d" % i)
                #showInfo ("@ Ending, y length is : %d" % len(y))
                i+=1
            answer = "".join(x)
            note[dst]=answer           

        except Exception, e:
            raise
        note.flush()
    Dictdb.close()
    mw.progress.finish()
    mw.reset()


def setupMenu(browser):
    a = QAction("Bulk-Generate RTK Vocab Reading Check", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onbulkCheckVocabReadingRTK(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onbulkCheckVocabReadingRTK(browser):
    bulkCheckVocabReadingRTK(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
