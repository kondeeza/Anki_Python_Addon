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
# Model name must contain this.
# each field name must be exact!
#Model name of the note type
modelName = ''
# The Field containing Japanese Vocab which you want to know the frequency ranking
Vocab_SrcField = ''
# Field to hold  the Freuency Ranking Goes here
dstField = ''
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
##########################################################################



def reload_config():
    global modelName
    global Vocab_SrcField
    global dstField
    global OVERWRITE_DST_FIELD

    config = mw.addonManager.getConfig(__name__)
    modelName = config['01_modelName']
    Vocab_SrcField = config['02_Vocab_SrcField']
    dstField = config['04_Output_SrcField']
    OVERWRITE_DST_FIELD= config['05_OVERWRITE_DST_FIELD']
    

def bulkGenerateVocabFq(nids):
    mw.checkpoint("bulk-Generate Vocab Fq")
    mw.progress.start()
    reload_config()
    FrequencyDBLocation = ""+os.path.dirname(__file__) + FrequencyDBSubfolderName + FrequencyDBname    
    FQdb = sqlite3.connect(FrequencyDBLocation)
    showInfo ("Beginning with the following config:\n modelName: %s \n Vocab_SrcField: %s \n dstField: %s \n OVERWRITE_DST_FIELD: %s \n" %(modelName,Vocab_SrcField,dstField,OVERWRITE_DST_FIELD ))
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            #showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
            continue
        src1 = None
        if Vocab_SrcField in note:
            src1 = Vocab_SrcField
        if not src1:
            # no src1 field
            #showInfo ("--> Field %s not found." % (Vocab_SrcField))
            continue
        dst = None
        if dstField in note:
            dst = dstField
        if not dst:
            #showInfo ("--> Field %s not found!" % (dstField))
            # no dst field
            continue
        if note[dst] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            #showInfo ("--> %s not empty. Skipping!" % (Vocab_SrcField))
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
            
        except Exception as e:
            raise
        note.flush()
    FQdb.close()
    mw.progress.finish()
    mw.reset()
    

    
def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('JP_Bulk-Generate Vocab Frequency')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateVocabFq(b))
    

def onBulkGenerateVocabFq(browser):
    bulkGenerateVocabFq(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
