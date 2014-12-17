'''
Created on 16/12/2014

@author: Myxoma
'''
from PyQt4 import QtGui, QtCore
import os

# Begin Manual Config
mSubfolderName = "\TestSubFolder\\"
mTextName = "testfile.txt"
#End manual Config
class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        #self.layout = QtGui.QGridLayout()
        layout = QtGui.QGridLayout(self)
        self.helloLabel = QtGui.QLabel("Say Hello To PyQT!")   
        self.helloLineEdit = QtGui.QLineEdit()   
        self.button1 = QtGui.QPushButton('Test', self)
        self.button1.clicked.connect(self.handleButton)
        TextFileLocation = ""+os.path.dirname(__file__) + mSubfolderName + mTextName    
        file = open(TextFileLocation, 'r')
        print file.read()
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.helloLabel, 0, 1)
        layout.addWidget(self.helloLineEdit, 1, 1)
        self.setWindowTitle("My Python App")
    def handleButton(self):
        print ('Hello World')


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())