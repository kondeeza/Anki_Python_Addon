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
import os
import csv

# Begin Manual Config
DictLocation = ""+os.path.dirname(__file__) + "\\Bulk_Generate_KrJp_def\\" + "KRDict_JP_All_Full_edited.csv"
#End manual Config

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.


##########################################################################
# Model name must contain this.
# each field name must be exact!
#Model name of the note type
modelName = 'Korean Vocab'
# The Field containing Japanese Vocab which you want to know the frequency ranking
Vocab_SrcField = 'Korean'
# Field to hold  the Freuency Ranking Goes here
dstField = 'Jp_Def'
debugMode = False
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
##########################################################################



def BulkGenerateKrJpDef(nids):
    mw.checkpoint("bulk-Generate Vocab Fq")
    mw.progress.start()
    
    with open(DictLocation, "r", encoding="utf-8")as tsvfile:
      reader = csv.DictReader(tsvfile,delimiter='\t', quoting=csv.QUOTE_NONE)
      #showInfo ("test mesg")

      defobj = {}
      for row in reader:
        #showInfo (str(row))
        #defobj[row[0]] = {"word": row[0], "jp_defs": row[1],"pos": row[2],"hanja": row[3],"jp_trans": row[4],"kr_trans": row[5]}
        if row['word'] in defobj:
            defobj[row['word']].append({"word": row["word"], "jp_defs": row["jp_defs"],"pos": row["pos"],"hanja": row["hanja"],"jp_trans": row["jp_trans"],"kr_trans": row["kr_trans"]})
        else:
            defobj[row['word']] = []
            defobj[row['word']].append({"word": row["word"], "jp_defs": row["jp_defs"],"pos": row["pos"],"hanja": row["hanja"],"jp_trans": row["jp_trans"],"kr_trans": row["kr_trans"]})
        
      #showInfo ("dict loaded")
      if (debugMode):
          showInfo (str(defobj['가가호호']))


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
            
            #showInfo (str(defobj["시내"]))
            #showInfo (str(defobj[''+vocabToQuery]))
            if (vocabToQuery != ""):
                """
                mQuery = "select freq from Dict where expression =\"" + vocabToQuery + "\";"
                cursor = FQdb.cursor()
                cursor.execute(mQuery)
                FQResult_Single = cursor.fetchone() #retrieve the first row
                if (FQResult_Single != None):
                    note[dst]=FQResult_Single[0]"""


                if vocabToQuery in defobj:
                    x = ""
                    if (debugMode):
                        showInfo (str(defobj[vocabToQuery]))
                    for defList in defobj[vocabToQuery]:
                        x += ", "+ defList["jp_defs"]
                    note[dst] = x
            
        except Exception as e:
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()
    

def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Bulk-Generate Kr Jp Def')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateKrJpDef(b))

def onBulkGenerateKrJpDef(browser):
    BulkGenerateKrJpDef(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
