#!/usr/bin/python3

#Messing around with a box that saves click locations and prints a list
#Basing the set-up and stuff on the ZetCode tutorials and some stack exchange posts

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#Classes
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #Picture widget
        #im = QImage()
        #imLabel = QLabel(self)
        #imLabel.setPixmap(QPixmap.fromImage(im))


        #Actions
        openFile = QAction(QIcon(),"&Open", self)
        openFile.setShortcut("Ctrl+O")
        openFile.triggered.connect(self.showOpenDialog)

        saveFile = QAction(QIcon(),"&Save", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.triggered.connect(self.showSaveDialog)

        exitAction = QAction(QIcon(),"&Quit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(qApp.quit)

        #Display
        menubar = self.menuBar()
        self.statusBar().showMessage("Waiting.")

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        self.resize(500,500)
        self.center()
        self.show()

    def center(self):
        winDim = self.frameGeometry()
        centPoint = QDesktopWidget().availableGeometry().center()
        winDim.moveCenter(centPoint)
        self.move(winDim.topLeft())

    def showOpenDialog(self):
        imname = QFileDialog.getOpenFileName(self, "Open Image", "/home")
        #i = open(imname)
        im = QImage()
        if im.load(imname[0]):
            imLabel = QLabel(self)
            imLabel.setPixmap(QPixmap.fromImage(im))
            self.setCentralWidget(imLabel)
            self.statusBar().showMessage("Image displayed.")
        else:
            self.statusBar().showMessage("Error")

    def showSaveDialog(self):
        pass

#Functions

#Main
if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
