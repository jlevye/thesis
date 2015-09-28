#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Continuing ZetCode tutorials, this on menus and toolbars

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QTextEdit
from PyQt5.QtGui import QIcon

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        textEdit = QTextEdit()displayed
        self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon("exit.png"), '&Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip("Exit Application") #What status should be displayed
        exitAction.triggered.connect(qApp.quit) #Makes the thing exit the thing

        self.statusBar() #Sticks a bar at the bottom (left justified) of the window

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        #An entirely redundant toolbar
        self.toolbar = self.addToolBar("Exit")
        self.toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("Hello world")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
