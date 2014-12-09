# -*- coding: utf-8 -*-
# Copyright: Chris Langewisch <ccl09c@my.fsu.edu>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Based on japanese.reading by Damien Elmes <anki@ichi2.net>
# Bulk copy data in one field to another.

##########################################################################
# USE LOWERCASE. Model name must contain this.
modelName = 'Japanese yomiSama'
# each field name must be exact!
VocabReading_SrcField = 'Vocab Reading'
VocabWithKanji_SrcField = 'Vocab'
dstField = 'Audio_Vocab_Japanese'
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
##########################################################################

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo

def bulkCopy(nids):
    mw.checkpoint("Bulk-copy Field")
    mw.progress.start()
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
            continue
        src1 = None
        if VocabReading_SrcField in note:
            src1 = VocabReading_SrcField
        if not src1:
            # no src1 field
            showInfo ("--> Field %s not found." % (VocabReading_SrcField))
            continue
        src2 = None
        if VocabWithKanji_SrcField in note:
            src2 = VocabWithKanji_SrcField
        if not src2:
            # no src2 field
            showInfo ("--> Field %s not found." % (VocabWithKanji_SrcField))
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
            showInfo ("--> %s not empty. Skipping!" % (VocabReading_SrcField))
            continue
        #srcTxt = mw.col.media.strip(note[src1])
        #if not srcTxt.strip():
        #    continue
        try:
            #showInfo ("--> Everything should have worked.")
            note[dst]="[sound:"+note[src1]+" - "+note[src2]+".mp3]"
            #note[dst] = srcTxt
        except Exception, e:
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    a = QAction("Bulk-Create JDIC audio syntax on Audio Field", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onBulkCopy(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onBulkCopy(browser):
    bulkCopy(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
