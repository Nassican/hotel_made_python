from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6 import QtGui, QtCore

import sys
import os
import json
import csv

def ui_login(self):
  if self.central_widget:
    self.central_widget.deleteLater()
    
  central_widget = QWidget(self)
  self.setCentralWidget(central_widget)
  # Crear un QFrame para el cuadro
  cuadro_frame = QWidget(self)
  cuadro_frame.setGeometry(100, 100, 400, 300)  # Ajusta la geometría según tus necesidades
  cuadro_frame.setStyleSheet("background-color: blue;")


  self.central_widget = cuadro_frame

