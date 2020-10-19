# -*- coding: utf-8 -*-
# Copyright: Chris Langewisch <ccl09c@my.fsu.edu>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Based on japanese.reading by Damien Elmes <anki@ichi2.net>
# Bulk copy data in one field to another.

##########################################################################
# USE LOWERCASE. Model name must contain this.
modelName = 'Japanese Epwing'
# each field name must be exact!
dstField = 'Audio_Vocab_Japanese'
folderPathToCheckCollection = r'D:\03-Japanese raw manga + Anime subs + Novel\more jap\SUper Jdic audio pack\JDIC_Audio_All_09April2010\extracted output'
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True
##########################################################################

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo
import os.path

def BulkDeleteEmptyJDICAudioField(nids):
    mw.checkpoint("Bulk-Delete Empty JDIC Audio Field")
    mw.progress.start()
    for nid in nids:
        #showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name']:
            showInfo ("--> Model mismatch: %s vs %s" %( modelName, note.model()['name']))
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
            showInfo ("--> %s not empty. Skipping!" % (dstField))
            continue
        if (note[dst] == ""):
            continue
        #srcTxt = mw.col.media.strip(note[src1])
        #if not srcTxt.strip():
        #    continue
        try:
            #showInfo ("--> Everything should have worked.")
            temp = unicode(note[dst])
            temp = temp.replace(u"[sound:", "")
            temp = temp.replace(u"]", "")
            FileToSearch = folderPathToCheckCollection + "\\" + temp
            #FileToSearch = unicode(FileToSearch)
            #showInfo ("File To Search is: %s" %(FileToSearch))
            if (os.path.isfile(FileToSearch) == False ):
                #showInfo ("Cannot Find it: %s" %(FileToSearch))
                note[dst]=""
                
            #note[dst]="[sound:"+note[src1]+" - .mp3]"
            #note[dst] = srcTxt
        except Exception, e:
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    a = QAction("Bulk-Delete Empty JDIC Audio Field", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onBulkDeleteEmptyJDICAudioField(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onBulkDeleteEmptyJDICAudioField(browser):
    BulkDeleteEmptyJDICAudioField(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
