#!/usr/bin/python3

#All classes/widgets besides main window for GUI
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PicBox(QLabel):
    @pyqtSlot(bool)
    def recordValue(self,b):
        return b

    def __init__(self,mainwin):
        super().__init__()
        self.initUI(mainwin)

    def initUI(self,mainwin):
        self.setScaledContents(True)
        self.setPixmap(QPixmap())
        self.mainwin = mainwin

        switch = self.mainwin.recordSignal.connect(self.recordValue)
        self.pointList = QListWidget()

    def showImage(self, image):
        self.setPixmap(QPixmap.fromImage(image))

    def status(self,mainwin):
         self.mainwin.statusBar().showMessage("{}",)
    #def status(self, switch):
    #    if switch:
    #        switch = False
    #    else:
    #        switch = True
    #    return switch

    def mousePressEvent(self,QMouseEvent,mainwin):
        point = (QMouseEvent.x(), QMouseEvent.y())
        self.mainwin.statusBar().showMessage("{0}".format(point))
        if self.mainwin.buttonbar.content.record.isChecked():
            self.pointlist.addItem(point)

class ButtonWidget(QWidget):
    def __init__(self,mainwin):
        super().__init__()
        self.initUI(mainwin)

    def initUI(self,mainwin):
        self.mainwin = mainwin
        hbox = QHBoxLayout()

        #Create the buttons
        record = QPushButton("Record")
        record.setCheckable(True)

        nodes = QPushButton("Nodes")
        nodes.clicked.connect(self.nodeList)

        hbox.addWidget(record)
        hbox.addWidget(nodes)
        self.setLayout(hbox)

    def nodeList(self):
        nodewin = ListDisplay(self.mainwin)
        nodewin.show()
        return nodewin

class ListDisplay(QDialog):
    def __init__(self,mainwin):
        super().__init__()

        self.mainwin = mainwin
        self.image = self.mainwin.imLabel
        self.list = self.image.pointList

        if self.image.picture == 0:
            lbl = QLabel("No image loaded.",self)
            lbl.move(15,10)
        else:
            x = 10
            for index in range(0,self.list.count()):
                lbl = QLabel(self.list.item(index),self)
                lbl.move(15,x)
                x += 10

        self.setWindowTitle("Nodes")
        self.setGeometry(300,300,100,150)
