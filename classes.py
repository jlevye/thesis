#!/usr/bin/python3

#All classes/widgets besides main window for GUI
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PicBox(QLabel):
    def __init__(self,mainwin):
        super().__init__()
        self.initUI(mainwin)

    def initUI(self,mainwin):
        #Sets up label with a null pixmap, a main window, and a list for points
        self.setPixmap(QPixmap())
        self.mainwin = mainwin
        self.pointList = list()

    def showImage(self, image):
        self.setPixmap(QPixmap.fromImage(image))

    def mousePressEvent(self, QMouseEvent):
        point = (QMouseEvent.x(), QMouseEvent.y())
        self.mainwin.statusBar().showMessage("{0}".format(point))
        if self.mainwin.buttonbar.record.isChecked():
            self.pointList.append(point)

    #This block of code has no current function - earlier attempts to set up recording functionality.
    #@pyqtSlot(bool)
    #def recordValue(self,b):
    #    return b
    #switch = self.mainwin.recordSignal.connect(self.recordValue)
    #def status(self,mainwin):
    #     self.mainwin.statusBar().showMessage("{}",)
    #def status(self, switch):
    #    if switch:
    #        switch = False
    #    else:
    #        switch = True
    #    return switch

class ButtonWidget(QWidget):
    def __init__(self,mainwin):
        super().__init__()
        self.initUI(mainwin)

    def initUI(self,mainwin):
        #Sets the main window/parent and a layout
        self.mainwin = mainwin
        hbox = QHBoxLayout()

        #Create the buttons
        self.record = QPushButton("Record")
        self.record.setCheckable(True)

        self.nodes = QPushButton("Nodes")
        self.nodes.clicked.connect(self.nodeList)

        #Fits the buttons to the layout
        hbox.addWidget(self.record)
        hbox.addWidget(self.nodes)
        self.setLayout(hbox)

    #Broken! Theoretically should pop up a window with stuff in it, but doesn't seem to work
    def nodeList(self):
        self.mainwin.nodewin = ListDisplay(self.mainwin)
        self.mainwin.nodewin.setWindowTitle("Nodes")
        self.mainwin.nodewin.setGeometry(300,300,100,150)
        self.mainwin.nodewin.show()
        #nodewin.show()
        #return nodewin

class ListDisplay(QDialog):
    def __init__(self,mainwin):
        super().__init__()
        self.initUI(mainwin)

    def initUI(self,mainwin):
        self.mainwin = mainwin
        self.image = self.mainwin.imLabel
        self.list = self.image.pointList

        if self.image.picture == 0:
            lbl = QLabel("No image loaded.",self)
            lbl.move(15,10)
        else:
            x = 10
            for item in self.list:
                lbl = QLabel(str(item),self)
                lbl.move(15,x)
                x += 10
