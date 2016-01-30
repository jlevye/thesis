#!/usr/bin/python3

#Messing around with a box that saves click locations and prints a list
#Basing the set-up and stuff on the ZetCode tutorials and some stack exchange posts

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#import graphtool
from classes import *

#Classes
class MainWindow(QMainWindow):
    recordSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Setting up widgets
        #Picture widget and scroll box to contain it - doesn't show until you load a picture
        self.imLabel = PicBox(self)
        self.scroll = QScrollArea()
        self.scroll.ensureVisible(self.geometry().x(), self.geometry().y())
        self.setCentralWidget(self.scroll)

        #Button Widget (Dockable 1)
        self.buttonbar = ButtonWidget(self)
        buttonDock = QDockWidget("Options")
        buttonDock.setWidget(self.buttonbar)
        self.addDockWidget(Qt.TopDockWidgetArea, buttonDock)

        #menus
        menubar = self.menuBar()

        #Menu actions
        openFile = QAction(QIcon(),"&Open", self)
        openFile.setShortcut("Ctrl+O")
        openFile.triggered.connect(lambda: self.showOpenDialog(self.imLabel))

        saveFile = QAction(QIcon(),"&Save", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.triggered.connect(self.showSaveDialog)

        exitAction = QAction(QIcon(),"&Quit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(qApp.quit)

        #File Menu Entries
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        #recordAction = QAction(QIcon(),"Record",self)
        #recordAction.setCheckable(True)
        #recordAction.toggled[bool].connect(self.recording)

        #Make a variable placeholder for a popup
        self.nodewin = None
        
        #Display the window
        self.resize(500,500)
        self.center()
        self.show()

    #Other Methods Used
    def center(self):
        winDim = self.frameGeometry()
        centPoint = QDesktopWidget().availableGeometry().center()
        winDim.moveCenter(centPoint)
        self.move(winDim.topLeft())

    def showOpenDialog(self,label):
        imname = QFileDialog.getOpenFileName(self, "Open Image", "/home")
        #i = open(imname)￼￼
        im = QImage()
        if im.load(imname[0]):
            label.showImage(im)
            self.scroll.setWidget(label)
            self.statusBar().showMessage("Image displayed.")
        else:
            self.statusBar().showMessage("Error")

    def showSaveDialog(self):
        pass

    def recording(self):
            self.recordSignal.emit()
            #self.statusBar().showMessage("Recording.")


#Main
if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    imbox = PicBox(win)
    sys.exit(app.exec_())
