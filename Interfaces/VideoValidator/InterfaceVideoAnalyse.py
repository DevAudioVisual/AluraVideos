import csv
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy, QAbstractItemView, QListWidget, QSlider, QVBoxLayout, QGridLayout,QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
import Util.CustomWidgets as cw

class InterfaceVideo(QWidget):
    def __init__(self):
        super().__init__() 
        self.layout = QVBoxLayout()
        self.layoutGrid = QGridLayout()
        
        self.check_frame_rate = cw.CheckBox("FPS")
        self.check_enquadramento = cw.CheckBox("Enquadramento")
        self.check_iluminação = cw.CheckBox("Iluminação")
        
        self.lista_widgets = [self.check_frame_rate,self.check_enquadramento,self.check_iluminação]
        
        row = 0
        column = 0
        for widget in self.lista_widgets:
          if row >= 3: 
            row = 0
            column +=1
          self.layoutGrid.addWidget(widget,row,column)
          row +=1
          
        self.layout.addLayout(self.layoutGrid)
        
        self.setLayout(self.layout)