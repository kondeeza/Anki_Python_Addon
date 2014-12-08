# -*- coding: utf-8 -*-
# Modified from "Quick Tagging" add-on
##########################################################################
# Model name must contain this.
modelName = 'Heisig'
# each field name must be exact!
Word_SrcField = 'Words'
dstField = 'Words_Clozed'
# if data exists in dstField, should we overwrite it?
OVERWRITE_DST_FIELD=True

# CONFIGURATION OPTIONS
generateClozedRTK_key = 't'
##########################################################################




from aqt import mw
from aqt.utils import getTag, tooltip, showInfo
from aqt.reviewer import Reviewer
# add space separated tags to a note
import re

def generateClozedRTK(nids):
    mw.checkpoint("Generate Clozed_RTK Note")
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
            TextOutput = re.sub('\((.*?)\)[:](.*?)(<br />)', "<br />", TextOutput)
            #showInfo(TextOutput)
            TextOutput = re.sub('\((.*?)\)[:](.*?)(<br/>)', "<br />", TextOutput)
            #showInfo(TextOutput)
            TextOutput = re.sub('\((.*?)\)[:](.*?)(<br>)', "<br />", TextOutput)
            #showInfo(TextOutput)
            TextOutput = re.sub('\((.*?)\)[:](.*)', "<br />", TextOutput)
            #showInfo(TextOutput)
            note[dst]= TextOutput
        except Exception, e:
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()

# replace _keyHandler in reviewer.py to add a keybinding
def newKeyHandler(self, evt):
    key = unicode(evt.text())
    note = mw.reviewer.card.note()
    if key == generateClozedRTK_key:
        
        #showInfo ("Found note: %s" % (self.card.note().id))
        generateClozedRTK([self.card.note().id])
        tooltip(_("Note Cloze Generated"))
    else:
        origKeyHandler(self, evt)

origKeyHandler = Reviewer._keyHandler
Reviewer._keyHandler = newKeyHandler

