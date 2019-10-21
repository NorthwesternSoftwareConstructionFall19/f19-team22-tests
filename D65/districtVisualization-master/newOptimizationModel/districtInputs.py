# -*- coding: utf-8 -*-
"""
Building GUI using PyQT package to collect user inputs
Created on Mon Jul 29 10:44:26 2019

@author: f3lix
"""

# import necessary packages
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# define GUI window
class getInputs(QWidget):
    def __init__(self):                                                         # intialize window
        super().__init__()
        self.title = 'Optimization inputs'
        self.initUI()
        self.setFocusPolicy(Qt.StrongFocus)
        
    def initUI(self):                                                           # define window properties
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 300, 500)
        vbox = QVBoxLayout()
        self.center()
        
        self.b1 = QPushButton("Average distance traveled")                      # objective switch 1: distance
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.o1 = 1
        self.b1.clicked.connect(self.o1off)
        vbox.addWidget(self.b1)
        
        self.s1 = QSlider(Qt.Horizontal, self)                                  # define slider widget for objective 1: distance
        self.s1.setFocusPolicy(Qt.NoFocus)
        self.s1.setRange(1, 3)
        self.s1.setValue(2)
        self.s1.setTickPosition(QSlider.TicksBelow)
        self.s1.setTickInterval(1)
        vbox.addWidget(self.s1)
        vbox.addStretch()
        
        self.b2 = QPushButton("Excess students over capacity")                  # objective switch 2: excess students
        self.b2.setCheckable(True)
        self.b2.toggle()
        self.o2 = 1
        self.b2.clicked.connect(self.o2off)
        vbox.addWidget(self.b2)
        
        self.s2 = QSlider(Qt.Horizontal, self)                                  # define slider widget for objective 2: excess students
        self.s2.setFocusPolicy(Qt.NoFocus)
        self.s2.setRange(1, 3)
        self.s2.setValue(2)
        self.s2.setTickPosition(QSlider.TicksBelow)
        self.s2.setTickInterval(1)
        vbox.addWidget(self.s2)
        vbox.addStretch()
        
        self.b3 = QPushButton("Number of buses required")                       # objective switch 2: excess students
        self.b3.setCheckable(True)
        self.b3.toggle()
        self.o3 = 1
        self.b3.clicked.connect(self.o3off)
        vbox.addWidget(self.b3)
        
        self.s3 = QSlider(Qt.Horizontal, self)                                  # define slider widget for objective 2: excess students
        self.s3.setFocusPolicy(Qt.NoFocus)
        self.s3.setRange(1, 3)
        self.s3.setValue(2)
        self.s3.setTickPosition(QSlider.TicksBelow)
        self.s3.setTickInterval(1)
        vbox.addWidget(self.s3)
        vbox.addStretch()
        
        hbox = QHBoxLayout()                                                    # quit and run buttons at bottom of window
        self.bq = QPushButton("Quit")
        self.bq.clicked.connect(self.close_app)
        self.bc = QPushButton("Run")
        self.bc.clicked.connect(self.get_output)
        hbox.addWidget(self.bq)
        hbox.addStretch()
        hbox.addWidget(self.bc)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        self.raise_()
        self.activateWindow()
    
    def center(self):                                                           # sub-function to find center of screen and center the window on it
        frameGeo = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frameGeo.moveCenter(center)
        self.move(frameGeo.topLeft())      
    
    def close_app(self):
        sys.exit()
        
    def o1off(self):
        self.o1 = 0
        return self.o1
    
    def o2off(self):
        self.o2 = 0
        return self.o2
    
    def o3off(self):
        self.o3 = 0
        return self.o3
    
    def get_output(self):
        self.scale1 = self.s1.value() * self.o1
        self.scale2 = self.s2.value() * self.o2
        self.scale3 = self.s3.value() * self.o3
        return self.scale1, self.scale2, self.scale3

# defining function to start the GUI for user input    
def districtInputs():        
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = getInputs()
        ex.show()
        sys.exit(app.exec_())