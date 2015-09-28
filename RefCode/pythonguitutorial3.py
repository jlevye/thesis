#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Continuing ZetCode tutorials - layout management

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QTextEdit

#First class defninition - absolute positioning
class Example1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lbl1 = QLabel("Hello",self)
        lbl1.move(15,10)

        lbl2 = QLabel("world",self)
        lbl2.move(35,40)

        lbl3 = QLabel("!!!",self)
        lbl3.move(55,70)

        self.setGeometry(300,300,250,250)
        self.setWindowTitle("Absolute")
        self.show()

#Second option - box model
class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        okButton = QPushButton("Ok")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1) #Makes the box stretch horizontally
        hbox.addWidget(okButton) #Automatically goes in lower right
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1) #Makes the box stretch so buttons stay in right vertical place
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300,300,250,250)
        self.setWindowTitle("Buttons")
        self.show()

#Third option - QGrid model
class Example3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ["Cls","Bck","","Close",
        "7","8","9","/",
        "4","5","6","*",
        "1","2","3","-",
        "0",".","=","+"]

        positions = [(i,j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name == "":
                continue
            button = QPushButton(name)
            grid.addWidget(button,*position)

        self.move(300,150)
        self.setWindowTitle("Calculator")
        self.show()

#More complicated grid example
class Example4(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = QLabel("Title")
        author = QLabel("Author")
        review = QLabel("Review")

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
        grid.addWidget(author, 1, 0)
        grid.addWidget(authorEdit, 2, 1)
        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

        self.setGeometry(300,300,350,300)
        self.setWindowTitle("Review")
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex1 = Example1()
    ex2 = Example2()
    ex3 = Example3()
    ex4 = Example4()
    sys.exit(app.exec())
