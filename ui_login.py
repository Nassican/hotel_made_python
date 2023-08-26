from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6 import QtGui, QtCore
from datetime import datetime

import sys
import os
import json
import csv


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
        cuadro_frame.setStyleSheet("background: transparent;")
        if self.central_widget:
          self.central_widget.deleteLater()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Crear un QFrame para el cuadro
        cuadro_frame = QWidget(self)
        cuadro_frame.setGeometry(100, 100, 400, 200)  
        cuadro_frame.setStyleSheet("background-color: blue;")
        self.central_widget = cuadro_frame

        cuadro_layout = QVBoxLayout(cuadro_frame)
        cuadro_layout.setContentsMargins(0, 0, 0, 0)   
        #TITULO
        titulo_label = QLabel("HOTEL SOFTPRO", cuadro_frame)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(255, 128, 128)) 
        titulo_label.setPalette(palette)
        font = QFont("Arial", 35, QFont.Bold)  # Fuente, tamaño, negrita
        titulo_label.setFont(font)
        cuadro_layout.addWidget(titulo_label)
        #CUADRO IZQUIERDA
        form_container = QWidget()
        form_container.setStyleSheet("background: transparent;")
        form_container.setMaximumWidth(350)

        layout_principal = QHBoxLayout()
   #    ETIQUETAS
        color1= ("font-size: 24px; font-weight: bold; color: green;")
        color= ("font-size: 24px; font-weight: bold;")

        etiqueta_estado = QLabel("Estado") 
        etiqueta_estado.setStyleSheet(color)#quita el fondo")
        campo_estado = QLineEdit()
        campo_estado.setText("ABIERTO")
        campo_estado.setStyleSheet("border: none;") 
        campo_estado.setStyleSheet(color1)
        #......................................
        #usado solo para espacio
        etiqueta_visitantes= QLabel("")
        etiqueta_visitantes.setStyleSheet(color)
        campo_huesped= QLineEdit()
        campo_huesped.setStyleSheet("border: none;") 

        etiqueta_info = QLabel("Informacion")
        etiqueta_info.setStyleSheet(color)
        campo_info = QLabel()
        campo_info.setStyleSheet("border: none;") 
        campo_info.setStyleSheet(color)
        campo_info.setText("BIENVENIDO! a gestion HOTEL SOFTPRO,<br>"
                            "")
        #campo_horas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        campo_info.setWordWrap(True)
        #--------------------
        self.campo_horac= QLabel()
        self.campo_horac.setStyleSheet("border: none;") 
        self.campo_horac.setStyleSheet(color)
         #-------------------------------------------------------
         #usada solo para espacio
        etiqueta_tiempo= QLabel("")
        etiqueta_tiempo.setStyleSheet(color)
        campo_tiempo= QLineEdit()
        campo_tiempo.setStyleSheet("border: none;") 
        #---------------------------------------
        no_ayuda = QLabel("Ayuda")
        no_ayuda.setStyleSheet("color: white;")
        self.no_ayuda = QComboBox()
        self.no_ayuda.setCursor(Qt.PointingHandCursor)
        self.no_ayuda.addItems(["Gestion Empleados", "Gestion Habitacion","Facturacion",])
        self.no_ayuda.setStyleSheet("QComboBox QAbstractItemView { color: white; }")
        self.no_ayuda.activated.connect(self.mostrar_ayuda)

        #-------------------------------------- 
        tiqueta_final = QLabel() 

        layout_formulario = QVBoxLayout()
        layout_formulario.addWidget(etiqueta_estado)
        layout_formulario.addWidget(campo_estado)
        layout_formulario.addWidget(etiqueta_visitantes)
        layout_formulario.addWidget(campo_huesped)
        layout_formulario.addWidget(etiqueta_info)
        layout_formulario.addWidget(campo_info)
        layout_formulario.addWidget(self.campo_horac)
        layout_formulario.addWidget(etiqueta_tiempo)
        layout_formulario.addWidget(no_ayuda)
        layout_formulario.addWidget(self.no_ayuda)
        layout_formulario.addWidget(tiqueta_final)

        form_container.setLayout(layout_formulario)

        layout_principal.addWidget(cuadro_frame)
        layout_principal.addWidget(form_container)
        #CUADRO PRINCIPAL
        central_widget = QWidget(self)
        central_widget.setLayout(layout_principal)
        central_widget.setMinimumSize(1100, 650)
        central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        bg_image_style = f"background-image: url(./icons/f5.png);"
        central_widget.setStyleSheet(bg_image_style)
        central_widget.setMinimumSize(1100, 650)
        self.timer.timeout.connect(lambda: self.actualizar_hora(self.campo_horac))


        self.setCentralWidget(central_widget)
        self.central_widget = central_widget


  

  
