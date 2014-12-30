# -*- coding: utf-8 -*-
'''
Created on 30/12/2014

@author: Myxoma
'''



from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from anki.hooks import addHook
#from aqt import mw
#from aqt.utils import showWarning, showInfo
import BulkCleanSongVoc.MultiVocabFieldUtil as MUtil


testInputUnicode = unicode(ur"<div>育む はぐくむ 25154&nbsp;(v5m,vt) to raise; to rear; to bring up<br /></div><div>asd</div>")

testInputUnicode = MUtil.CleaNnbsp(testInputUnicode)
MUtil.CleanDivSyntaxToBR(testInputUnicode)