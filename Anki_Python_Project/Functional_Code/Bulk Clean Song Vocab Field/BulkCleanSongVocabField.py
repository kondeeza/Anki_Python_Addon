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


testInputUnicode = unicode(ur"<div><div>朝礼 ちょうれい 34100&nbsp;morning assembly (company, school, etc.); pep talk</div><div>dfg<br /><div>ミサ 12464&nbsp;(n) (Catholic) mass (like an assembly hall)</div></div></div><div>zxc</div><div>sdf</div><div>asd</div><div>gd</div><div>s</div><div>df</div><div>sdf</div><div>dsf</div><div>d</div>")

testInputUnicode = MUtil.CleaNnbsp(testInputUnicode)
MUtil.CleanDivSyntaxToBR(testInputUnicode)