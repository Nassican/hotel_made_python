from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6 import QtGui, QtCore
from datetime import datetime
import pytz

import sys
import os
import json
import csv
import pytz


class OutlineLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) 
        painter.setPen(QColor(225, 225, 255))  # Color negro para el contorno
        painter.drawText(event.rect(), self.alignment(), self.text())
        painter.setPen(self.palette().color(QPalette.WindowText))  # Restaurar el color de texto original
       # painter.drawText(event.rect(), Qt.AlignmentFlag.AlignCenter, self.text())


def ui_login(self):
  #CUADRO DERECHA
  cuadro_frame = QWidget(self)
  cuadro_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
  #cuadro_frame.setGeometry(10, 10, 1200, 600)  # Ajusta la geometría según tus necesidades
  #cuadro_frame.setStyleSheet("background-color:red;")
  cuadro_frame.setStyleSheet("background: transparent;")

  cuadro_layout = QVBoxLayout(cuadro_frame)
  cuadro_layout.setContentsMargins(0, 0, 0, 0) 
  #cuadro_layout.setStyleSheet("background-color: transparent;")
  
  #TITULO
  titulo_label = QLabel("HOTEL SOFTPRO", cuadro_frame)
  titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto horizontalmente
   
  palette = QPalette()
  palette.setColor(QPalette.WindowText, QColor(255, 0, 0))  # Color de texto rojo
  #palette.setColor(QPalette.Window, QColor(0, 0, 255))  # Color de fondo azul
  titulo_label.setPalette(palette)

  font = QFont("Arial", 20, QFont.Bold)  # Fuente, tamaño, negrita
  titulo_label.setFont(font)
  
  cuadro_layout.addWidget(titulo_label)
  #CUADRO IZQUIERDA
  form_container = QWidget()
  form_container.setStyleSheet("background: transparent;")
  form_container.setMaximumWidth(300)

  layout_principal = QHBoxLayout()
 #ETIQUETAS
  color= ("font-size: 24px; font-weight: bold;")

  etiqueta_estado = OutlineLabel("Estado") 
  etiqueta_estado.setStyleSheet( color)#quita el fondo")
  campo_estado = QLineEdit()
  etiqueta_visitantes= OutlineLabel("huespedes")
  etiqueta_visitantes.setStyleSheet(color)
  campo_huesped= QLineEdit()

  etiqueta_horas=OutlineLabel("bogota")
  etiqueta_horas.setStyleSheet(color)
  campo_horas=QLineEdit()
  campo_horas.setStyleSheet(color)
  tz_horas=pytz.timezone("US/Eastern")
  current_time_horas= datetime.now(tz_horas)
  hora_hrs= current_time_horas.strftime("%H:%M:%S %Z")
  campo_horas.setText(hora_hrs)

  etiqueta_hora= OutlineLabel("HORA")
  etiqueta_hora.setStyleSheet(color)
  campo_horac= QLineEdit()
  campo_horac.setStyleSheet(color)
  tz_colombia = pytz.timezone("US/Eastern")
  current_time_colombia= datetime.now(tz_colombia)
  hora_colombia = current_time_colombia.strftime("%H:%M:%S %Z")
  campo_horac.setText(hora_colombia)
  #--------------------------------------------------------
  etiqueta_hra= OutlineLabel("hola")
  etiqueta_hra.setStyleSheet(color)
  campo_hra= QLineEdit()
  campo_hra.setStyleSheet(color)
  tz_central = pytz.timezone("US/Central")
  current_time_central= datetime.now(tz_central)
  hora_central = current_time_central.strftime("%H:%M:%S %Z")
  campo_hra.setText(hora_central)
   #-------------------------------------------------------
  etiqueta_tiempo= OutlineLabel("hora3")
  etiqueta_tiempo.setStyleSheet(color)
  campo_tiempo= QLineEdit()
  campo_tiempo.setStyleSheet(color)
  tz_pacific = pytz.timezone("US/Pacific")
  current_time_pacific= datetime.now(tz_pacific)
  hora_pacific = current_time_pacific.strftime("%H:%M:%S %Z")
  campo_tiempo.setText(hora_pacific)
  #-------------------------------------- 
  tiqueta_final = QLabel() 

  layout_formulario = QVBoxLayout()
  layout_formulario.addWidget(etiqueta_estado)
  layout_formulario.addWidget(campo_estado)
  layout_formulario.addWidget(etiqueta_visitantes)
  layout_formulario.addWidget(campo_huesped)
  layout_formulario.addWidget(etiqueta_horas)
  layout_formulario.addWidget(campo_horas)
  layout_formulario.addWidget(etiqueta_hora)
  layout_formulario.addWidget(campo_horac)
  layout_formulario.addWidget(etiqueta_hra)
  layout_formulario.addWidget(campo_hra)
  layout_formulario.addWidget(etiqueta_tiempo)
  layout_formulario.addWidget(campo_tiempo)
  layout_formulario.addWidget(tiqueta_final)

  form_container.setLayout(layout_formulario)

  layout_principal.addWidget(cuadro_frame)
  layout_principal.addWidget(form_container)
  #CUADRO PRINCIPAL
  central_widget= QWidget(self)
  central_widget.setLayout(layout_principal)
  central_widget.setMinimumSize(1100, 650)
  central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
  #central_widget.setGeometry(100, 100, 1200, 800) 
  #cuadro_frame.setLayout(layout_principal)
  bg_image_style = f"background-image: url(./icons/f5.png); background-size: {central_widget.width()}px {central_widget.height()}px;"
  central_widget.setStyleSheet(bg_image_style)
  #central_widget.setStyleSheet("background-image: url(./icons/f5.png); background-size: cover; ") 
  central_widget.setMinimumSize(1100, 650)
  #central_widget.adjustSize()

  #central_widget.setStyleSheet("background-image: url(./icons/fonda.png);") 
  self.setCentralWidget(central_widget)
