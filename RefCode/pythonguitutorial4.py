#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Continuing ZetCode tutorials - dialogues

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Example1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn1 = QPushButton("Name",self)
        self.btn1.move(20,20)
        self.btn1.clicked.connect(self.showNameDialog)

        self.btn2 = QPushButton("Color",self)
        self.btn2.move(20,54)
        self.btn2.clicked.connect(self.showColorDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        col = QColor(0,0,0)
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget {background-color: %s}" % col.name())
        self.frm.setGeometry(130,56,142,32)


        self.setGeometry(300,300,290,150)
        self.setWindowTitle("Dialog Examples")
        self.show()

    def showNameDialog(self):
        text, ok = QInputDialog.getText(self, "Input Dialog", "Enter Your Name: ")
        if ok:
            self.le.setText(str(text))

    def showColorDialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex1 = Example1()
    sys.exit(app.exec_())
