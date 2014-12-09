# -*- coding: utf-8 -*-
'''
Created on 09/12/2014

@author: Myxoma
'''

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, showWarning
# import all of the Qt GUI library
from aqt.qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
import sqlite3
import os

# Begin Manual Config
FrequencyDBSubfolderName = "\Bulk_Generate_Vocab_Frequency\\"
FrequencyDBname = "freq.sqlite"
#End manual Config

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.


##########################################################################
# USE LOWERCASE. Model name must contain this.
modelName = 'Japanese yomiSama'
# each field name must be exact!
Vocab_SrcField = 'Vocab'
dstField = 'Frequency Ranking'
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
##########################################################################



def bulkGenerateVocabFq(nids):
    mw.checkpoint("bulk-Generate Vocab Fq")
    mw.progress.start()
    
    FrequencyDBLocation = ""+os.path.dirname(__file__) + FrequencyDBSubfolderName + FrequencyDBname    
    FQdb = sqlite3.connect(FrequencyDBLocation)

    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
            continue
        src1 = None
        if Vocab_SrcField in note:
            src1 = Vocab_SrcField
        if not src1:
            # no src1 field
            showInfo ("--> Field %s not found." % (Vocab_SrcField))
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
            showInfo ("--> %s not empty. Skipping!" % (Vocab_SrcField))
            continue
        #srcTxt = mw.col.media.strip(note[src1])
        #if not srcTxt.strip():
        #    continue
        try:
            #showInfo ("--> Everything should have worked.")
            #vocabToQuery = "相当"
            vocabToQuery = note[src1]
            if (vocabToQuery != ""):
                mQuery = "select freq from Dict where expression =\"" + vocabToQuery + "\";"
                cursor = FQdb.cursor()
                cursor.execute(mQuery)
                FQResult_Single = cursor.fetchone() #retrieve the first row
                if (FQResult_Single != None):
                    note[dst]=FQResult_Single[0]
            
        except Exception, e:
            raise
        note.flush()
    FQdb.close()
    mw.progress.finish()
    mw.reset()
    

def setupMenu(browser):
    a = QAction("Bulk-Generate Vocab Frequency", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onBulkGenerateVocabFq(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onBulkGenerateVocabFq(browser):
    bulkGenerateVocabFq(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
