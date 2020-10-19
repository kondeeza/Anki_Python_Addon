# -*- coding: utf-8 -*-
# Copyright: Chris Langewisch <ccl09c@my.fsu.edu>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Based on japanese.reading by Damien Elmes <anki@ichi2.net>
# Bulk copy data in one field to another.

##########################################################################
# USE LOWERCASE. Model name must contain this.
modelName = 'Heisig'
# each field name must be exact!
Word_SrcField = 'Words'
dstField = 'Words_Clozed'
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
DONT_INCLUDE_MARKED_DUPLICATES = True
##########################################################################

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo
import re

def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set( x for x in seq if x in seen or seen_add(x) )
    # turn the set into a list (as requested)
    return list( seen_twice )
def quickGenerateSameWordHighlight(nids):
    mw.checkpoint("quick GenerateSameWordHighlight")
    mw.progress.start()
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
            x = []
            for i in y:
                if (i.find("*") ==-1 and i.find("^") ==-1):
                    x.append(i + "<br />")
                if ((i.find("*") !=-1 or i.find("^") !=-1) and DONT_INCLUDE_MARKED_DUPLICATES == False ):
                    x.append(i + "<br />")
            if (len(x) !=0):
                x.pop()
            x = list_duplicates(x)
            x = "".join(x)
            answer = x
            note[dst]= answer
        except Exception, e:
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    a = QAction("Quick generate SameWordHighlight", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: OnquickGenerateSameWordHighlight(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def OnquickGenerateSameWordHighlight(browser):
    quickGenerateSameWordHighlight(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
