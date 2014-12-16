# -*- coding: utf-8 -*-
'''
Created on 16/12/2014

@author: Myxoma
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PyQt4 import QtGui, QtCore
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo

class MWidgetMaker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.button = QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton)
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

    def handleButton(self):
        print ('Hello World')

def TestWidget():
    mw.checkpoint("Test Widget")
    mw.progress.start()
    mw.myWidget = mTestWidget = MWidgetMaker()
    mTestWidget.show()
    mw.progress.finish()
    mw.reset()
def setupMenu(browser):
    a = QAction("Test Widget", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onTestWidget(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onTestWidget(browser):
    TestWidget()

addHook("browser.setupMenus", setupMenu)