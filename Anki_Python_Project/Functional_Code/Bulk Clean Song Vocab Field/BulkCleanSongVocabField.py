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
testInputUnicode = unicode(ur"<div><div>朝礼 ちょうれい 34100&nbsp;morning assembly (company, school, etc.); pep talk</div><div><div>ミサ 12464&nbsp;(n) (Catholic) mass (like an assembly hall)</div></div></div>")

outputUnicode = MUtil.AutoCleanField(testInputUnicode,True,debugMode = True)

