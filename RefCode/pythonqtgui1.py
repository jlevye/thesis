#!/usr/bin/python3
# -*- coding: utf-8 -*-

#PyQt tutorial, putting all the examples from "First programs in PyQt5" via ZetCode in one application window. 

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication

class Example(QWidget): #This line creates a class that inherits from QWidget

    def __init__(self):
        super().__init__() #gets it from the parent class

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont("SansSerif", 10))
        qbtn = QPushButton("Perma-quit", self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.setToolTip("I quit you.")
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50,50)

        #self.setGeometry(300,300,250,250) #gives size and position in one command instead of 2; commented out to show centering
        self.resize(250,250)
        self.center()

        self.setWindowTitle("Hello World")
        self.setWindowIcon(QIcon("web.png"))

        self.show()

    #There already exists a close event handler for a widget class. This lets us re-implement that to behave how we want. Doesn't change behavior of that button.
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry() #Gets the dimensions of our application window
        cp = QDesktopWidget().availableGeometry().center() #Finds the center of the desktop
        qr.moveCenter(cp) #Centers our rectangle on the screen
        self.move(qr.topLeft()) #Puts the window in that rectangle

if __name__ == '__main__': #Then this is the actual main section of the code

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
