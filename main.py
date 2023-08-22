from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6 import QtGui, QtCore
from ui_login import ui_login

import sys
import os
import json
import csv

class HabitacionWindow(QDialog):
    def __init__(self, habitaciones, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Habitación")
        
        self.lista_habitaciones = QListWidget(self)
        self.lista_habitaciones.itemClicked.connect(self.habitacion_seleccionada_changed)

        for habitacion in habitaciones:
            if habitacion['estado'] == "Disponible":
                item_text = f"N°: {habitacion['n_habitacion']} - {habitacion['estado']} - {habitacion['tipo_de_habitacion']}"
                item = QListWidgetItem(item_text)

                item.setData(Qt.UserRole, habitacion['n_habitacion'])  # Usar UserRole para guardar información personalizada
                item.setData(Qt.UserRole + 1, habitacion['tipo_de_habitacion'])

                self.lista_habitaciones.addItem(item)

        self.lista_habitaciones.adjustSize()  # Autoajustar tamaño del QListWidget
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok, parent=self)
        self.button_box.setCursor(Qt.PointingHandCursor)
        self.button_box.accepted.connect(self.accept)
        encabezado = QLabel("N° Habitación - Estado - Tipo")
        layout = QVBoxLayout()
        layout.addWidget(encabezado)
        layout.addWidget(self.lista_habitaciones)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def habitacion_seleccionada_changed(self, item):
        if item.flags() & Qt.ItemIsSelectable:  # Verificar si el elemento es seleccionable
            n_habitacion = item.data(Qt.UserRole)
            tipo_habitacion = item.data(Qt.UserRole + 1)
            self.habitacion_seleccionada = (n_habitacion, tipo_habitacion)
            print(f"Habitación seleccionada: {self.habitacion_seleccionada}")

class HabitacionesWindowMultiple(QDialog):
    def __init__(self, habitaciones, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Habitaciones")

        self.lista_habitaciones = QListWidget(self)
        self.lista_habitaciones.itemClicked.connect(self.habitacion_seleccionada_changed)

        for habitacion in habitaciones:
            if habitacion['estado'] == "Disponible":
                item_text = f"N°: {habitacion['n_habitacion']} - {habitacion['estado']} - {habitacion['tipo_de_habitacion']}"
                item = QListWidgetItem(item_text)

                item.setData(Qt.UserRole, habitacion['n_habitacion'])  # Usar UserRole para guardar información personalizada
                item.setData(Qt.UserRole + 1, habitacion['tipo_de_habitacion'])

                self.lista_habitaciones.addItem(item)

        self.lista_habitaciones.setSelectionMode(QListWidget.MultiSelection)  # Permitir selección múltiple
        self.lista_habitaciones.adjustSize()  # Autoajustar tamaño del QListWidget

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok, parent=self)
        self.button_box.setCursor(Qt.PointingHandCursor)
        self.button_box.accepted.connect(self.accept)

        encabezado = QLabel("N° Habitación - Estado - Tipo")
        layout = QVBoxLayout()
        layout.addWidget(encabezado)
        layout.addWidget(self.lista_habitaciones)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def habitacion_seleccionada_changed(self, item):
        if not (item.data(Qt.UserRole + 2) == "Disponible"):
            item.setSelected(False)
        else:
            n_habitacion = item.data(Qt.UserRole)
            tipo_habitacion = item.data(Qt.UserRole + 1)
            if (n_habitacion, tipo_habitacion) not in self.habitaciones_seleccionadas:
                self.habitaciones_seleccionadas.append((n_habitacion, tipo_habitacion))
            else:
                self.habitaciones_seleccionadas.remove((n_habitacion, tipo_habitacion))
            print("Habitaciones seleccionadas:", self.habitaciones_seleccionadas)        

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Hotel Infinito")
        self.setMinimumSize(1000, 550)
        self.setWindowIcon(QtGui.QIcon('./icons/hotel-logo.png'))
        styles = ''
        self.app = QApplication.instance()


        self.reservas_data = []
        self.habitaciones_data = []
        self.selected_habitaciones = []

        exitAction = QtGui.QAction(QtGui.QIcon('./icons/x-mark-64.png'), 'Salir', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)

        reserva_ui = QtGui.QAction(QtGui.QIcon('./icons/recepcion.png'), 'Reservas', self)
        reserva_ui.triggered.connect(self.reservas_recepcion_ui)

        reserva_ui2 = QtGui.QAction(QtGui.QIcon('./icons/square-rounded-64.png'), 'Reservas', self)
        reserva_ui2.triggered.connect(self.gestion_habitacion_ui)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(reserva_ui)
        self.toolbar.addAction(reserva_ui2)
        self.toolbar.addAction(exitAction)
        self.toolbar.setMovable(False)

        main_menu = self.menuBar()
        archivo_menu = main_menu.addMenu("Archivo")

        sub_menu = archivo_menu.addMenu("Temas")  # Agregar un submenú
        sub_action1 = QAction("Fusion", self)
        sub_action1.triggered.connect(lambda: self.set_app_style("Fusion"))
        sub_action2 = QAction("Windows", self)
        sub_action2.triggered.connect(lambda: self.set_app_style("Windows"))
        sub_menu.addAction(sub_action1)
        sub_menu.addAction(sub_action2)
        

        self.central_widget = None
        
        ui_login(self)

    def set_app_style(self, style):
        app.setStyle(style)


    def reservas_recepcion_ui(self):
        self.setStyleSheet(open('styles.qss').read())
        if self.central_widget:
            self.central_widget.deleteLater()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.longitud_minima = 10
        main_layout = QHBoxLayout(central_widget)

        # Formulario en la izquierda
        form_container = QWidget()
        form_container.setMaximumWidth(320)  # Ancho máximo deseado
        form_layout = QVBoxLayout(form_container)

        grid_layout = QGridLayout()

        int_validator = QIntValidator()

        nombre_label = QLabel("Nombre: *")
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")

        identificacion_label = QLabel("Identificación: *")
        self.identificacion_input = QLineEdit()
        self.identificacion_input.setMaxLength(10)
        self.identificacion_input.textChanged.connect(self.validar_longitud_minima)
        
        self.identificacion_input.setValidator(int_validator)
        self.identificacion_input.setPlaceholderText("Ej: 1234567890")

        contacto_label = QLabel("Contacto: *")
        self.contacto_input = QLineEdit()
        self.contacto_input.setMaxLength(10)
        self.contacto_input.textChanged.connect(self.validar_longitud_minima)
        self.contacto_input.setValidator(int_validator)

        fecha_entrada_label = QLabel("Entrada: *")
        self.fecha_entrada_input = QDateEdit()
        self.fecha_entrada_input.setCursor(Qt.PointingHandCursor)
        self.fecha_entrada_input.setCalendarPopup(True)
        self.fecha_entrada_input.setDisplayFormat("dd/MM/yyyy")
        self.fecha_entrada_input.setDate(QDate.currentDate())

        fecha_salida_label = QLabel("Salida:")
        self.fecha_salida_input = QDateEdit()
        self.fecha_salida_input.setCursor(Qt.PointingHandCursor)
        self.fecha_salida_input.setCalendarPopup(True)
        self.fecha_salida_input.setDisplayFormat("dd/MM/yyyy")
        self.fecha_salida_input.setDate(QDate.currentDate())

        tipo_habitacion_label = QLabel("Tipo de Habitación: *")
        self.tipo_habitacion_input = QPushButton("Escoger habitación")
        self.tipo_habitacion_input.clicked.connect(self.abrir_ventana_habitacion)
        self.tipo_habitacion_input.setCursor(Qt.PointingHandCursor)
        self.info_habitacion = QLabel("N° Habitación: - Tipo:")

        self.mas_de_una_habitacion_checkbox = QCheckBox("Más habitaciónes:")
        self.mas_de_una_habitacion_checkbox.setCursor(Qt.PointingHandCursor)

        self.escoger_habitaciones = QPushButton("Escoger habitaciónes")
        self.escoger_habitaciones.clicked.connect(self.open_multi_select_window)
        self.escoger_habitaciones.setCursor(Qt.PointingHandCursor)
        self.escoger_habitaciones.setEnabled(False)

        self.info_mas_habitaciones = QLabel("N° Habitación: - Tipo:")
        self.info_mas_habitaciones.setWordWrap(True)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.info_mas_habitaciones.setSizePolicy(size_policy)
        
        self.scroll_area = QListWidget()


        def toggle_cantidad_habitaciones(checked):
            self.escoger_habitaciones.setEnabled(checked)
            if not checked:
                self.scroll_area.clear()

        self.mas_de_una_habitacion_checkbox.stateChanged.connect(toggle_cantidad_habitaciones)

        huespedes_label = QLabel("N° Huespuedes: *")
        self.huespedes_input = QLineEdit()
        self.huespedes_input.setValidator(int_validator)
        self.huespedes_input.setPlaceholderText("N° Huespuedes")
        habitaciones_disponibles = self.contar_habitaciones_disponibles()
        self.huespedes_input.setPlaceholderText(f"N° Huespedes (Max: {habitaciones_disponibles})")

        formato_pago_label = QLabel("Forma de Pago: *")
        self.formato_pago_input = QComboBox()
        self.formato_pago_input.setCursor(Qt.PointingHandCursor)
        self.formato_pago_input.setPlaceholderText("Forma de Pago")
        self.formato_pago_input.addItems(["Tarjeta de Credito", "Tarjeta de Debito", "Efectivo"])

        

        # Agregar elementos al grid_layout
        grid_layout.addWidget(nombre_label, 0, 0)  # Fila 0, Columna 0
        grid_layout.addWidget(self.nombre_input, 0, 1)  # Fila 0, Columna 1
        grid_layout.addWidget(identificacion_label, 1, 0)  
        grid_layout.addWidget(self.identificacion_input, 1, 1)  
        grid_layout.addWidget(contacto_label, 2, 0)
        grid_layout.addWidget(self.contacto_input, 2, 1)
        grid_layout.addWidget(fecha_entrada_label, 3, 0)
        grid_layout.addWidget(self.fecha_entrada_input, 3, 1)
        grid_layout.addWidget(fecha_salida_label, 4, 0)
        grid_layout.addWidget(self.fecha_salida_input, 4, 1)
        grid_layout.addWidget(tipo_habitacion_label, 5, 0)
        grid_layout.addWidget(self.tipo_habitacion_input, 5, 1)
        grid_layout.addWidget(self.info_habitacion, 6, 1)
        grid_layout.addWidget(self.mas_de_una_habitacion_checkbox, 7, 0)
        grid_layout.addWidget(self.escoger_habitaciones, 7, 1)
        grid_layout.addWidget(self.scroll_area, 8, 1)
        grid_layout.addWidget(huespedes_label, 9, 0)
        grid_layout.addWidget(self.huespedes_input, 9, 1)
        grid_layout.addWidget(formato_pago_label, 10, 0)
        grid_layout.addWidget(self.formato_pago_input, 10, 1)

        # Agregar el grid_layout al form_layout
        titulo = QLabel("Agregar Cliente")
        titulo.setMaximumHeight(70)
        titulo.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 20px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(titulo)

        form_layout.addLayout(grid_layout)
        form_layout.setAlignment(grid_layout, Qt.AlignTop)

        # Metodo Buscar
        grid_layout_buscar = QGridLayout()
        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Buscar por nombre o identificación")
        self.buscar_input.textChanged.connect(self.buscar_clientes)

        grid_layout_buscar.addWidget(self.buscar_input, 0, 0)

        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.setCursor(Qt.PointingHandCursor)
        self.guardar_button.clicked.connect(self.guardar_reserva)
        self.guardar_button.clicked.connect(lambda: self.actualizar_tabla(self.table))

        editar_button = QPushButton("Editar Fila")
        editar_button.setCursor(Qt.PointingHandCursor)
        editar_button.clicked.connect(self.editar_fila)

        form_layout.addSpacing(0)

        form_layout.addLayout(grid_layout_buscar)
        form_layout.addWidget(self.guardar_button)
        form_layout.addWidget(editar_button)

        # Tabla en la derecha
        self.table = QTableWidget(self)
        self.table.setWordWrap(True)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["Nombre", "Identificación", "Contacto", "Entrada", "Salida", "N° Habitacion - Tipo", "Mas Habitaciones", "N° Habitaciones - Tipo", "N° Huespedes", "FormaPago"])
        self.table.setRowCount(0)
        self.cargar_datos(self.table)
        main_layout.addWidget(form_container)

        # Configurar la tabla como no editable
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(30)  # Cambia el tamaño de las filas
        self.table.verticalHeader().setMinimumSectionSize(30)
        self.table.resizeRowsToContents()
        main_layout.addWidget(self.table)


        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header_section = header.sectionSize(i)
            header.setStyleSheet(f"QHeaderView::section {{ padding: 5px; font-size: 14px;}}")
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            header.setMinimumSectionSize(header_section)
            header.setDefaultSectionSize(header_section)


        self.central_widget = main_layout

    def gestion_habitacion_ui(self):
        self.setStyleSheet(open('styles.qss').read())
        if self.central_widget:
            self.central_widget.deleteLater()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.longitud_minima = 10
        main_layout = QHBoxLayout(central_widget)

        # Formulario en la izquierda
        form_container = QWidget()
        form_container.setMaximumWidth(320)  # Ancho máximo deseado
        form_layout = QVBoxLayout(form_container)

        grid_layout = QGridLayout()

        int_validator = QIntValidator()

        no_habitacion_label = QLabel("N° Habitacion:")
        self.no_habitacion_input = QComboBox()
        self.no_habitacion_input.setCursor(Qt.PointingHandCursor)
        self.no_habitacion_input.addItems(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                                           "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                                           "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                                           "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",])

        estado_label = QLabel("Estado:")
        self.estado_input = QComboBox()
        self.estado_input.setCursor(Qt.PointingHandCursor)
        self.estado_input.setPlaceholderText("Estado")
        self.estado_input.addItems(["Disponible", "En proceso de limpieza", "Ocupada", "Fuera de servicio"])

        tipo_habitacion_label = QLabel("Tipo de Habitación:")
        self.tipo_habitacion_input = QComboBox()
        self.tipo_habitacion_input.setCursor(Qt.PointingHandCursor)
        self.tipo_habitacion_input.setPlaceholderText("Tipo de Habitación")
        self.tipo_habitacion_input.addItems(["Doble", "Suite"])

        self.actualizar_estado_habitacion_button = QPushButton("Actualizar")
        self.actualizar_estado_habitacion_button.setCursor(Qt.PointingHandCursor)
        self.actualizar_estado_habitacion_button.clicked.connect(self.guardar_habitaciones)
        

        

        # Agregar elementos al grid_layout
        grid_layout.addWidget(no_habitacion_label, 0, 0)  # Fila 0, Columna 0
        grid_layout.addWidget(self.no_habitacion_input, 0, 1)  # Fila 0, Columna 1
        grid_layout.addWidget(estado_label, 1, 0)  
        grid_layout.addWidget(self.estado_input, 1, 1) 
        grid_layout.addWidget(tipo_habitacion_label, 2, 0)
        grid_layout.addWidget(self.tipo_habitacion_input, 2, 1)

        # Agregar el grid_layout al form_layout
        titulo = QLabel("Gestión de Habitaciones")
        titulo.setWordWrap(True)
        titulo.setMaximumHeight(100)
        titulo.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 20px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(titulo)

        form_layout.addLayout(grid_layout)
        form_layout.setAlignment(grid_layout, Qt.AlignTop)

        # Metodo Buscar
        grid_layout_buscar = QGridLayout()
        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Buscar por numero de habitación o por Estado")
        # self.buscar_input.textChanged.connect(self.buscar_habitacion)

        grid_layout_buscar.addWidget(self.buscar_input, 0, 0)


        form_layout.addSpacing(0)

        form_layout.addLayout(grid_layout_buscar)
        form_layout.addWidget(self.actualizar_estado_habitacion_button)

        # Tabla en la derecha
        self.table_habitaciones = QTableWidget(self)
        self.table_habitaciones.setWordWrap(True)
        self.table_habitaciones.setColumnCount(3)
        self.table_habitaciones.setHorizontalHeaderLabels(["N° de Habitacion", "Estado", "Tipo de Habitación"])
        self.table_habitaciones.setRowCount(0)
        self.cargar_datos_habitaciones(self.table_habitaciones)
        main_layout.addWidget(form_container)

        # Configurar la tabla como no editable
        self.table_habitaciones.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_habitaciones.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_habitaciones.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_habitaciones.verticalHeader().setDefaultSectionSize(30)  # Cambia el tamaño de las filas
        self.table_habitaciones.horizontalHeader().setDefaultSectionSize(200)
        self.table_habitaciones.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(self.table_habitaciones)



        header = self.table_habitaciones.horizontalHeader()
        for i in range(self.table_habitaciones.columnCount()):
            header_section = header.sectionSize(i)
            header.setStyleSheet(f"QHeaderView::section {{ padding: 5px; font-size: 14px; font-weight: bold;}}")
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            header.setMinimumSectionSize(header_section)
            header.setDefaultSectionSize(header_section)

        self.central_widget = main_layout


    # FUNCIONES PARA GUARDAR LAS RECEPCIONES-RESERVACIONES -----------------
    def guardar_reserva(self):
        nombre = self.nombre_input.text()
        identificacion = self.identificacion_input.text()
        contacto = self.contacto_input.text()
        fecha_entrada = self.fecha_entrada_input.date()
        
        numero_huespedes = self.huespedes_input.text()
        forma_pago = self.formato_pago_input.currentText()

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Campo Vacío")
        ok_button = msg_box.addButton("Ok", QMessageBox.AcceptRole)
        ok_button.setCursor(Qt.PointingHandCursor)

        total_habitaciones = ""
        for habitacion in self.selected_habitaciones:
            n_habitacion = habitacion[0]
            tipo_habitacion = habitacion[1]
            total_habitaciones += ''.join(f'N°: {habitacion[0]} - Tipo: {habitacion[1]}\n')
            


        if not nombre:
            msg_box.setText("Por favor, ingrese un nombre.")
            # Agregar el botón "Ok" y configurar el cursor
            msg_box.exec()
            return
        elif not identificacion:
            msg_box.setText("Por favor, ingrese una identificación.")
            msg_box.exec()
            return
        elif len(identificacion) < 10:
            msg_box.setText("Por favor, ingrese una identificación correcta.")
            msg_box.exec()
            return
        elif not contacto:
            msg_box.setText("Por favor, ingrese un numero de contacto.")
            msg_box.exec()
            return
        elif len(contacto) < 10:
            msg_box.setText("Por favor, ingrese un numero de contacto correcto.")
            msg_box.exec()
            return
        elif not fecha_entrada:
            msg_box.setText("Por favor, ingrese una fecha de entrada.")
            msg_box.exec()
            return
        
        try:
            n_habitacion, tipo_habitacion = self.habitacion_seleccionada
        except AttributeError:
            msg_box.setText("Por favor, escoja una habitación.")
            msg_box.exec()
            return

        if not n_habitacion:
            msg_box.setText("Por favor, escoja una habitación.")
            msg_box.exec()
            return
        
        if self.mas_de_una_habitacion_checkbox.isChecked():
            if not total_habitaciones:
                QMessageBox.warning(self, "Campo Vacío", "Por favor, escoja las habitaciones.")
                return

        if not numero_huespedes:
            msg_box.setText("Por favor, ingrese el numero de huespedes.")
            msg_box.exec()
            return
        elif not forma_pago:
            msg_box.setText("Por favor, ingrese una forma de pago.")
            msg_box.exec()
            return
        
    
        reserva = {
            "nombre": self.nombre_input.text(),
            "identificacion": self.identificacion_input.text(),
            "contacto": self.contacto_input.text(),
            "entrada": self.fecha_entrada_input.date().toString("dd/MM/yyyy"),
            "salida": self.fecha_salida_input.date().toString("dd/MM/yyyy"),
            "n_t_habitacion": f"N°: {n_habitacion} - Tipo: {tipo_habitacion}",
            "mas_habitaciones": self.mas_de_una_habitacion_checkbox.isChecked(),
            "total_habitaciones": total_habitaciones,
            "huespedes": self.huespedes_input.text(),
            "forma_pago": self.formato_pago_input.currentText()
        }
        self.reservas_data.append(reserva)
        
        self.guardar_datos_csv()

    def guardar_datos_csv(self):
        with open("datos_reservas.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            headers = ["Nombre", "Identificación", "Contacto", "Entrada", "Salida", "N° Habitación -Tipo", "Mas Habitaciones", "N° Habitaciones - Tipo" , "N° Huespedes", "FormaPago"]
            csvwriter.writerow(headers)
            for reserva in self.reservas_data:
                row = [
                    reserva["nombre"],
                    reserva["identificacion"],
                    reserva["contacto"],
                    reserva["entrada"],
                    reserva["salida"],
                    reserva["n_t_habitacion"],
                    "Sí" if reserva["mas_habitaciones"] else "No",
                    reserva["total_habitaciones"],
                    reserva["huespedes"],
                    reserva["forma_pago"]
                ]
                csvwriter.writerow(row)

    def actualizar_tabla(self, table):
        table.setRowCount(len(self.reservas_data))
        for row, reserva in enumerate(self.reservas_data):
            table.setItem(row, 0, QTableWidgetItem(reserva["nombre"],))
            table.setItem(row, 1, QTableWidgetItem(reserva["identificacion"]))
            table.setItem(row, 2, QTableWidgetItem(reserva["contacto"]))
            table.setItem(row, 3, QTableWidgetItem(reserva["entrada"]))
            table.setItem(row, 4, QTableWidgetItem(reserva["salida"]))
            table.setItem(row, 5, QTableWidgetItem(reserva["n_t_habitacion"]))
            table.setItem(row, 6, QTableWidgetItem("Sí" if reserva["mas_habitaciones"] else "No"))
            table.setItem(row, 7, QTableWidgetItem(reserva["total_habitaciones"]))
            table.setItem(row, 8, QTableWidgetItem(reserva["huespedes"]))
            table.setItem(row, 9, QTableWidgetItem(reserva["forma_pago"]))

            table.resizeRowsToContents()

    def cargar_datos(self, table):
        try:
            with open("datos_reservas.csv", "r", newline="") as csvfile:
                csvreader = csv.reader(csvfile)
                headers = next(csvreader)
                self.reservas_data = []
                for row in csvreader:
                    reserva = {
                        "nombre": row[0],
                        "identificacion": row[1],
                        "contacto": row[2],
                        "entrada": row[3],
                        "salida": row[4],
                        "n_t_habitacion": row[5],
                        "mas_habitaciones": row[6] == "Sí",
                        "total_habitaciones": row[7],
                        "huespedes": row[8],
                        "forma_pago": row[9]
                    }
                    self.reservas_data.append(reserva)
                self.actualizar_tabla(table)
        except FileNotFoundError:
            pass

    # Funcion para verificar longitud minima identificacion
    def validar_longitud_minima(self):
            texto = self.identificacion_input.text()
            if len(texto) < self.longitud_minima:
                self.identificacion_input.setStyleSheet("border: 1px solid red;")
            else:
                self.identificacion_input.setStyleSheet("border: 1px solid #ccc;")

    def actualizar_maximo_habitaciones(self, tipo_habitacion):
        if tipo_habitacion == "Doble":
            self.cantidad_habitaciones_input.setPlaceholderText("Cantidad (Max 30)")
        elif tipo_habitacion == "Suite":
            self.cantidad_habitaciones_input.setPlaceholderText("Cantidad (Max 10)")

    def validar_cantidad_habitaciones(self):
        max_value = 30 if self.tipo_habitaciones.currentText() == "Doble" else 10
        cantidad = self.cantidad_habitaciones_input.text()
        if not cantidad.isdigit():
            self.cantidad_habitaciones_input.clear()
        elif int(cantidad) > max_value:
            self.cantidad_habitaciones_input.setText(str(max_value))


    # Funcion para editar la fila que seleccionemos
    def editar_fila(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            selected_items = self.table.selectedItems()
            if len(selected_items) > 0:
                row_data = []
                for item in selected_items:
                    row_data.append(item.text())
                # Rellenar los campos de edición con los valores de la fila seleccionada
                self.nombre_input.setText(row_data[0])
                self.identificacion_input.setText(row_data[1])
                self.contacto_input.setText(row_data[2])
                self.fecha_entrada_input.setDate(QDate.fromString(row_data[3], "dd/MM/yyyy"))   
                self.fecha_salida_input.setDate(QDate.fromString(row_data[4], "dd/MM/yyyy"))  

                self.info_habitacion.setText(row_data[5])

                self.mas_de_una_habitacion_checkbox.setChecked(row_data[6] == "Sí") 
                item_column_7 = self.table.item(selected_row, 7)
                
                if item_column_7 is not None:
                    self.scroll_area.clear()
                    column_7_text = item_column_7.text()
                    items_column_7 = column_7_text.split('\n')
                    # Agregar cada elemento al QListWidget
                    for item in items_column_7:
                        if item.strip():  # Ignorar elementos vacíos
                            list_widget_item = QListWidgetItem(item.strip())
                            self.scroll_area.addItem(list_widget_item)
                self.huespedes_input.setText(row_data[8])
                self.formato_pago_input.setCurrentText(row_data[9])
                self.guardar_button.setText("Guardar Edición")
                # Conectar el botón "Guardar Edición" a la función de edición
                self.guardar_button.clicked.disconnect()
                self.guardar_button.clicked.connect(lambda: self.guardar_edicion(selected_row))

    def guardar_edicion(self, row):
        nombre = self.nombre_input.text()
        identificacion = self.identificacion_input.text()
        contacto = self.contacto_input.text()
        fecha_entrada = self.fecha_entrada_input.date()
        
        numero_huespedes = self.huespedes_input.text()
        forma_pago = self.formato_pago_input.currentText()

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Campo Vacío")
        ok_button = msg_box.addButton("Ok", QMessageBox.AcceptRole)
        ok_button.setCursor(Qt.PointingHandCursor)

        total_habitaciones = ""
        for habitacion in self.selected_habitaciones:
            n_habitacion = habitacion[0]
            tipo_habitacion = habitacion[1]
            total_habitaciones += ''.join(f'N°: {habitacion[0]} - Tipo: {habitacion[1]}\n')
            


        if not nombre:
            msg_box.setText("Por favor, ingrese un nombre.")
            # Agregar el botón "Ok" y configurar el cursor
            msg_box.exec()
            return
        elif not identificacion:
            msg_box.setText("Por favor, ingrese una identificación.")
            msg_box.exec()
            return
        elif len(identificacion) < 10:
            msg_box.setText("Por favor, ingrese una identificación correcta.")
            msg_box.exec()
            return
        elif not contacto:
            msg_box.setText("Por favor, ingrese un numero de contacto.")
            msg_box.exec()
            return
        elif len(contacto) < 10:
            msg_box.setText("Por favor, ingrese un numero de contacto correcto.")
            msg_box.exec()
            return
        elif not fecha_entrada:
            msg_box.setText("Por favor, ingrese una fecha de entrada.")
            msg_box.exec()
            return
        
        try:
            n_habitacion, tipo_habitacion = self.habitacion_seleccionada
        except AttributeError:
            msg_box.setText("Por favor, escoja una habitación.")
            msg_box.exec()
            return

        if not n_habitacion:
            msg_box.setText("Por favor, escoja una habitación.")
            msg_box.exec()
            return
        
        if self.mas_de_una_habitacion_checkbox.isChecked():
            if not total_habitaciones:
                QMessageBox.warning(self, "Campo Vacío", "Por favor, escoja las habitaciones.")
                return

        if not numero_huespedes:
            msg_box.setText("Por favor, ingrese el numero de huespedes.")
            msg_box.exec()
            return
        elif not forma_pago:
            msg_box.setText("Por favor, ingrese una forma de pago.")
            msg_box.exec()
            return
        
    
        self.reservas_data[row] = {
            "nombre": self.nombre_input.text(),
            "identificacion": self.identificacion_input.text(),
            "contacto": self.contacto_input.text(),
            "entrada": self.fecha_entrada_input.date().toString("dd/MM/yyyy"),
            "salida": self.fecha_salida_input.date().toString("dd/MM/yyyy"),
            "n_t_habitacion": f"N°: {n_habitacion} - Tipo: {tipo_habitacion}",
            "mas_habitaciones": self.mas_de_una_habitacion_checkbox.isChecked(),
            "total_habitaciones": total_habitaciones,
            "huespedes": self.huespedes_input.text(),
            "forma_pago": self.formato_pago_input.currentText()
        }

        # Guardar los datos actualizados en el archivo CSV
        self.guardar_datos_csv()

        # Restaurar el texto del botón "Guardar"
        self.guardar_button.setText("Guardar")

        # Actualizar la tabla con los datos editados
        self.actualizar_tabla(self.table)

    # Funcion para buscar clientes
    def buscar_clientes(self):
            buscar_texto = self.buscar_input.text()

            if not buscar_texto:  # Si el campo de búsqueda está vacío
                self.actualizar_tabla(self.table)
                return

            resultados = []
            for reserva in self.reservas_data:
                if buscar_texto.lower() in reserva["nombre"].lower():
                    resultados.append(reserva)
                if buscar_texto.lower() in reserva["identificacion"].lower():
                    resultados.append(reserva)
                    
            if resultados:
                self.actualizar_tabla_buscar(self.table, resultados)
            else:
                QMessageBox.information(self, "Búsqueda", "No se encontraron resultados.")
    
    def actualizar_tabla_buscar(self, table, data):
        table.setRowCount(len(data))
        for row, reserva in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(reserva["nombre"],))
            table.setItem(row, 1, QTableWidgetItem(reserva["identificacion"]))
            table.setItem(row, 2, QTableWidgetItem(reserva["contacto"]))
            table.setItem(row, 3, QTableWidgetItem(reserva["entrada"]))
            table.setItem(row, 4, QTableWidgetItem(reserva["salida"]))
            table.setItem(row, 5, QTableWidgetItem(reserva["n_t_habitacion"]))
            table.setItem(row, 6, QTableWidgetItem("Sí" if reserva["mas_habitaciones"] else "No"))
            table.setItem(row, 7, QTableWidgetItem(reserva["total_habitaciones"]))
            table.setItem(row, 8, QTableWidgetItem(reserva["huespedes"]))
            table.setItem(row, 9, QTableWidgetItem(reserva["forma_pago"]))

        table.resizeRowsToContents()
    
    def contar_habitaciones_disponibles(self):
        contador = 0
        for habitacion in self.habitaciones_data:
            if habitacion["estado"] == "Disponible":
                contador += 1
        return contador
    
    def obtener_habitaciones(self):
        return self.habitaciones_data

    def abrir_ventana_habitacion(self):
        habitacion_window = HabitacionWindow(self.habitaciones_data, parent=self)
        if habitacion_window.exec():
            # Si se ha seleccionado una habitación
            self.habitacion_seleccionada = habitacion_window.habitacion_seleccionada
            if self.habitacion_seleccionada is not None:
                n_habitacion, tipo_habitacion = self.habitacion_seleccionada
                self.info_habitacion.setText(f"N°: {n_habitacion} - Tipo: {tipo_habitacion}")
                print(n_habitacion, tipo_habitacion)
        else:
            print("No hay habitaciones disponible, No se escogio ninguna habitacion")


    def open_multi_select_window(self):  # Datos de las habitaciones
        habitaciones_window = HabitacionesWindowMultiple(self.habitaciones_data, self)
        result = habitaciones_window.exec()
        if result == QDialog.Accepted:
            selected_items = habitaciones_window.lista_habitaciones.selectedItems()
            new_selected_habitaciones = [(item.data(Qt.UserRole), item.data(Qt.UserRole + 1)) for item in selected_items]

            for habitacion in new_selected_habitaciones:
                if habitacion not in self.selected_habitaciones:
                    self.selected_habitaciones.append(habitacion)    
            
            self.change_label_habitaciones()
            print("Habitaciones seleccionadas:", self.selected_habitaciones)

    def change_label_habitaciones(self):
        if len(self.selected_habitaciones) != 0:
            self.scroll_area.clear()

            for habitacion in self.selected_habitaciones:
                self.item_text = f"N°: {habitacion[0]} - Tipo: {habitacion[1]}"
                item = QListWidgetItem(self.item_text)
                self.scroll_area.addItem(item)


    # FUNCIONES PARA GUARDAR LAS HABITACIONES -----------------
    def guardar_habitaciones(self):
        n_habitacion = self.no_habitacion_input.currentText()
        estado = self.estado_input.currentText()
        tipo_habitacion = self.tipo_habitacion_input.currentText()

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Campo Vacío")
        ok_button = msg_box.addButton("Ok", QMessageBox.AcceptRole)
        ok_button.setCursor(Qt.PointingHandCursor)

        if not n_habitacion:
            msg_box.setText("Por favor, ingrese un numero de habitacion valido.")
            # Agregar el botón "Ok" y configurar el cursor
            msg_box.exec()
            return
        elif not estado:
            msg_box.setText("Por favor, ingrese un estado valido.")
            msg_box.exec()
            return
        elif not tipo_habitacion:
            msg_box.setText("Por favor, ingrese un tipo de habitación valido.")
            msg_box.exec()
            return
    
        existing_reserva = None
        for reserva in self.habitaciones_data:
            if reserva["n_habitacion"] == n_habitacion:
                existing_reserva = reserva
                break

        if existing_reserva:
            # Si ya existe, actualiza el estado en lugar de agregar una nueva entrada
            existing_reserva["estado"] = estado
            existing_reserva["tipo_de_habitacion"] = tipo_habitacion
        else:
            reserva = {
                "n_habitacion": n_habitacion,
                "estado": estado,
                "tipo_de_habitacion": tipo_habitacion,
            }
            self.habitaciones_data.append(reserva)
        
        self.guardar_datos_csv_habitaciones()
        self.actualizar_tabla_habitacion(self.table_habitaciones)

    def guardar_datos_csv_habitaciones(self):
        with open("datos_habitaciones.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            headers = ["N° Habitacion", "Estado", "Tipo de Habitación"]
            csvwriter.writerow(headers)
            for habitacion in self.habitaciones_data:
                row = [
                    habitacion["n_habitacion"],
                    habitacion["estado"],
                    habitacion["tipo_de_habitacion"]
                ]
                csvwriter.writerow(row)

    def actualizar_tabla_habitacion(self, table):
        # Ordena la lista self.habitaciones_data por la columna "N° Habitación"
        self.habitaciones_data.sort(key=lambda x: int(x["n_habitacion"]))
        table.setRowCount(len(self.habitaciones_data))
        for row, reserva in enumerate(self.habitaciones_data):
            table.setItem(row, 0, QTableWidgetItem(reserva["n_habitacion"]))
            table.setItem(row, 1, QTableWidgetItem(reserva["estado"]))
            table.setItem(row, 2, QTableWidgetItem(reserva["tipo_de_habitacion"]))

            if reserva["estado"] == "Disponible":
                table.item(row, 1).setBackground(QtGui.QColor(50, 205, 50))  # Verde
            elif reserva["estado"] == "En proceso de limpieza":
                table.item(row, 1).setBackground(QtGui.QColor(255, 215, 0))  # Amarillo
            elif reserva["estado"] == "Ocupada":
                table.item(row, 1).setBackground(QtGui.QColor(139, 0, 0))  # Rojo
                table.item(row, 1).setForeground(QtGui.QColor(255, 255, 255))  # Letras blancas
            elif reserva["estado"] == "Fuera de servicio":
                table.item(row, 1).setBackground(QtGui.QColor(184, 134, 11))  # Marrón
            
            if reserva["tipo_de_habitacion"] == "Doble":
                table.item(row, 2).setBackground(QtGui.QColor(0, 191, 255))  # Azul
                table.item(row, 2).setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            elif reserva["tipo_de_habitacion"] == "Suite":
                table.item(row, 2).setBackground(QtGui.QColor(255, 105, 180))
                table.item(row, 2).setForeground(QtGui.QColor(255, 255, 255))  # Letras blancas
                # Letras Bold
                table.item(row, 2).setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Ajustar a contenido en la columna 0
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        table.resizeRowsToContents()
        table.resizeColumnsToContents()

    def cargar_datos_habitaciones(self, table):
        try:
            with open("datos_habitaciones.csv", "r", newline="") as csvfile:
                csvreader = csv.reader(csvfile)
                try:
                    headers = next(csvreader)
                except StopIteration:
                    pass

                self.habitaciones_data = []
                for row in csvreader:
                    habitacion = {
                        "n_habitacion": row[0],
                        "estado": row[1],
                        "tipo_de_habitacion": row[2],
                    }
                    self.habitaciones_data.append(habitacion)

                if not self.habitaciones_data:
                    self.llenar_habitaciones_disponibles()

                self.actualizar_tabla_habitacion(table)

        except FileNotFoundError:
            self.llenar_habitaciones_disponibles()

    def actualizar_estado_habitacion(self, numero_habitacion, nuevo_estado):
        # Buscar la fila correspondiente en la tabla de habitaciones
        for row in range(self.table_habitaciones.rowCount()):
            numero_habitacion_actual = self.table_habitaciones.item(row, 0).text()
            if numero_habitacion_actual == numero_habitacion:
                # Actualizar el estado de la habitación en la tabla de habitaciones
                item_estado = QTableWidgetItem(nuevo_estado)
                self.table_habitaciones.setItem(row, 1, item_estado)
                break
        
    def marcar_habitacion_como_ocupada(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
           numero_habitacion = self.table.item(selected_row, 5).text()  # Suponiendo que el número de habitación está en la columna 5
           nuevo_estado = "Ocupada"
           self.actualizar_estado_habitacion(numero_habitacion, nuevo_estado)
           # 
    

    def llenar_habitaciones_disponibles(self):
        self.habitaciones_data = []
        for index in range(1, 41):  # Rango de habitaciones del 1 al 40
            n_habitacion = f"{index:02}"  # Formato de dos dígitos, por ejemplo, "01", "02", ..., "40"
            tipo = "Doble" if index <= 30 else "Suite"  # Determinar el tipo de habitación
            habitacion = {
                "n_habitacion": n_habitacion,
                "estado": "Disponible",
                "tipo_de_habitacion": tipo,  # Agregar el tipo de habitación
            }
            self.habitaciones_data.append(habitacion)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
