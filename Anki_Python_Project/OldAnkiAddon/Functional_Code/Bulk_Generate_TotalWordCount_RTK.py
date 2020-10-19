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
dstField = 'Total_Word_Counts'
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
##########################################################################

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo
import re
def BulkGenerateTotalWordCountRTK(nids):
    mw.checkpoint("Bulk-Generate TotalWordCount")
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
            brformat1count = TextOutput.count("<br />")
            brformat2count = TextOutput.count("<br/>")
            brformat3count = TextOutput.count("<br>")
            TotalWordCount = brformat1count + brformat2count + brformat3count
            if (TextOutput != ""):
                TotalWordCount = TotalWordCount+1
                note[dst]= str(TotalWordCount)
        except Exception, e:
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    a = QAction("Bulk-Generate TotalWordCount RTK data Field", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onBulkGenerateTotalWordCountRTK(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onBulkGenerateTotalWordCountRTK(browser):
    BulkGenerateTotalWordCountRTK(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
