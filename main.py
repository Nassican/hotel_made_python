from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6 import QtGui
import sys
import os
import json
import csv

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Hotel Infinito")
        self.setMinimumSize(1000, 550)
        self.setWindowIcon(QtGui.QIcon('./icons/hotel-logo.png'))
        styles = ''
        self.app = QApplication.instance()


        self.reservas_data = []

        exitAction = QtGui.QAction(QtGui.QIcon('./icons/x-mark-64.png'), 'Salir', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)

        reserva_ui = QtGui.QAction(QtGui.QIcon('./icons/recepcion.png'), 'Reservas', self)
        reserva_ui.triggered.connect(self.reservas_recepcion_ui)

        reserva_ui2 = QtGui.QAction(QtGui.QIcon('./icons/square-rounded-64.png'), 'Reservas', self)
        reserva_ui2.triggered.connect(self.reservas)

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
        
        self.ui_login()

    def set_app_style(self, style):
        app.setStyle(style)

    def ui_login(self):
        # Crear un QFrame para el cuadro
        cuadro_frame = QWidget(self)
        cuadro_frame.setGeometry(100, 100, 400, 300)  # Ajusta la geometría según tus necesidades
        cuadro_frame.setStyleSheet("background-color: lightblue;")

        self.central_widget = cuadro_frame


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
        self.fecha_entrada_input.setCalendarPopup(True)
        self.fecha_entrada_input.setDisplayFormat("dd/MM/yyyy")
        self.fecha_entrada_input.setDate(QDate.currentDate())

        fecha_salida_label = QLabel("Salida:")
        self.fecha_salida_input = QDateEdit()
        self.fecha_salida_input.setCalendarPopup(True)
        self.fecha_salida_input.setDisplayFormat("dd/MM/yyyy")
        self.fecha_salida_input.setDate(QDate.currentDate())

        tipo_habitacion_label = QLabel("Tipo de Habitación: *")
        self.tipo_habitacion_input = QComboBox()
        self.tipo_habitacion_input.setPlaceholderText("Tipo de Habitación")
        self.tipo_habitacion_input.addItems(["Doble", "Suite"])

        self.mas_de_una_habitacion_checkbox = QCheckBox("Más habitaciónes:")
        self.cantidad_habitaciones_input = QLineEdit()
        self.cantidad_habitaciones_input.setPlaceholderText("Cantidad (max 30)")
        self.cantidad_habitaciones_input.setEnabled(False)

        self.tipo_habitaciones = QComboBox()
        self.tipo_habitaciones.setPlaceholderText("Tipos de Habitaciónes")
        self.tipo_habitaciones.addItems(["Doble", "Suite"])
        self.tipo_habitaciones.setEnabled(False)

        def toggle_cantidad_habitaciones(checked):
            self.cantidad_habitaciones_input.setEnabled(checked)
            self.tipo_habitaciones.setEnabled(checked)
            if not checked:
                self.cantidad_habitaciones_input.clear()
                self.actionEventtipo_habitaciones.clear()

        self.mas_de_una_habitacion_checkbox.stateChanged.connect(toggle_cantidad_habitaciones)

        huespedes_label = QLabel("N° Huespuedes: *")
        self.huespedes_input = QLineEdit()

        formato_pago_label = QLabel("Forma de Pago: *")
        self.formato_pago_input = QComboBox()
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
        grid_layout.addWidget(self.mas_de_una_habitacion_checkbox, 6, 0)
        grid_layout.addWidget(self.cantidad_habitaciones_input, 6, 1)
        grid_layout.addWidget(self.tipo_habitaciones, 7, 1)
        grid_layout.addWidget(huespedes_label, 8, 0)
        grid_layout.addWidget(self.huespedes_input, 8, 1)
        grid_layout.addWidget(formato_pago_label, 9, 0)
        grid_layout.addWidget(self.formato_pago_input, 9, 1)

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

        guardar_button = QPushButton("Guardar")
        guardar_button.clicked.connect(self.guardar_reserva)
        guardar_button.clicked.connect(lambda: self.actualizar_tabla(self.table))


        form_layout.addSpacing(0)

        form_layout.addLayout(grid_layout_buscar)
        form_layout.addWidget(guardar_button)

        # Tabla en la derecha
        self.table = QTableWidget(self)
        self.table.setWordWrap(True)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["Nombre", "Identificación", "Contacto", "Entrada", "Salida", "TipoHabitacion", "Mas Habitaciones", "Cantidad Habitaciones", "N° Huespedes", "FormaPago"])
        self.table.setRowCount(0)
        self.cargar_datos(self.table)
        main_layout.addWidget(form_container)

        # Configurar la tabla como no editable
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setDefaultSectionSize(30)  # Cambia el tamaño de las filas
        self.table.verticalHeader().setMinimumSectionSize(30)
        main_layout.addWidget(self.table)



        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header_section = header.sectionSize(i)
            header.setStyleSheet(f"QHeaderView::section {{ padding: 5px; font-size: 14px;}}")
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            header.setMinimumSectionSize(header_section)
            header.setDefaultSectionSize(header_section)


        self.central_widget = main_layout

    
    def validar_longitud_minima(self):
        texto = self.identificacion_input.text()
        if len(texto) < self.longitud_minima:
            self.identificacion_input.setStyleSheet("border: 1px solid red;")
        else:
            self.identificacion_input.setStyleSheet("border: 1px solid #ccc;")


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



    def reservas(self):
        if self.central_widget:
            self.central_widget.deleteLater()
            
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Formulario en la izquierda
        form_layout = QVBoxLayout()

        nombre_label = QLabel("Nsdadsadasd:")
        nombre_input = QLineEdit()
        apellido_label = QLabel("Apellasdsadadido:")
        apellido_input = QLineEdit()
        guardar_button = QPushButton("Guaasdasdsadrdar")

        form_layout.addWidget(nombre_label)
        form_layout.addWidget(nombre_input)
        form_layout.addWidget(apellido_label)
        form_layout.addWidget(apellido_input)
        form_layout.addWidget(guardar_button)

        # Tabla en la derecha
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nombsadsadare", "Apeasdadsllido", "Aasdasdcción"])
        table.setRowCount(0)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(table)

        self.central_widget = main_layout
    


    # FUNCIONES PARA GUARDAR LAS RECEPCIONES-RESERVACIONES
    def guardar_reserva(self):
        nombre = self.nombre_input.text()
        identificacion = self.identificacion_input.text()
        contacto = self.contacto_input.text()
        fecha_entrada = self.fecha_entrada_input.date()
        tipo_habitacion = self.tipo_habitacion_input.currentText()
        numero_huespedes = self.huespedes_input.text()
        forma_pago = self.formato_pago_input.currentText()

        if not nombre:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese un nombre.")
            return
        elif not identificacion:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese una identificación.")
            return
        elif len(identificacion) < 10:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese una identificación correcta.")
            return
        elif not contacto:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese un numero de contacto.")
            return
        elif len(contacto) < 10:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese un numero de contacto correcto.")
            return
        elif not fecha_entrada:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese una fecha de entrada.")
            return
        elif not tipo_habitacion:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese un tipo de habitación.")
            return
        elif not numero_huespedes:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese el numero de huespedes.")
            return
        elif not forma_pago:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese una forma de pago.")
            return
        
        if self.mas_de_una_habitacion_checkbox.isChecked():
            cantidad_habitaciones = self.cantidad_habitaciones_input.text()
            tipo_habitaciones = self.tipo_habitaciones.currentText()
            if not cantidad_habitaciones:
                QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese una cantidad de habitaciones.")
                return
            elif not tipo_habitaciones:
                QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese un tipo de habitaciones.")
                return
    
        reserva = {
            "nombre": self.nombre_input.text(),
            "identificacion": self.identificacion_input.text(),
            "contacto": self.contacto_input.text(),
            "entrada": self.fecha_entrada_input.date().toString("dd/MM/yyyy"),
            "salida": self.fecha_salida_input.date().toString("dd/MM/yyyy"),
            "tipo_habitacion": self.tipo_habitacion_input.currentText(),
            "mas_habitaciones": self.mas_de_una_habitacion_checkbox.isChecked(),
            "cantidad_habitaciones": self.cantidad_habitaciones_input.text(),
            "tipo_habitaciones": self.tipo_habitaciones.currentText(),
            "huespedes": self.huespedes_input.text(),
            "forma_pago": self.formato_pago_input.currentText()
        }
        self.reservas_data.append(reserva)
        
        self.guardar_datos_csv()

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
                        "tipo_habitacion": row[5],
                        "mas_habitaciones": row[6] == "Sí",
                        "cantidad_habitaciones": row[7],
                        "huespedes": row[8],
                        "forma_pago": row[9]
                    }
                    self.reservas_data.append(reserva)
                self.actualizar_tabla(table)
        except FileNotFoundError:
            pass

    def actualizar_tabla_buscar(self, table, data):
        table.setRowCount(len(data))
        for row, reserva in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(reserva["nombre"]))
            table.setItem(row, 1, QTableWidgetItem(reserva["identificacion"]))
            table.setItem(row, 2, QTableWidgetItem(reserva["contacto"]))
            table.setItem(row, 3, QTableWidgetItem(reserva["entrada"]))
            table.setItem(row, 4, QTableWidgetItem(reserva["salida"]))
            table.setItem(row, 5, QTableWidgetItem(reserva["tipo_habitacion"]))
            table.setItem(row, 6, QTableWidgetItem("Sí" if reserva["mas_habitaciones"] else "No"))
            table.setItem(row, 7, QTableWidgetItem(reserva["cantidad_habitaciones"]))
            table.setItem(row, 8, QTableWidgetItem(reserva["huespedes"]))
            table.setItem(row, 9, QTableWidgetItem(reserva["forma_pago"]))

    def actualizar_tabla(self, table):
        table.setRowCount(len(self.reservas_data))
        for row, reserva in enumerate(self.reservas_data):
            table.setItem(row, 0, QTableWidgetItem(reserva["nombre"]))
            table.setItem(row, 1, QTableWidgetItem(reserva["identificacion"]))
            table.setItem(row, 2, QTableWidgetItem(reserva["contacto"]))
            table.setItem(row, 3, QTableWidgetItem(reserva["entrada"]))
            table.setItem(row, 4, QTableWidgetItem(reserva["salida"]))
            table.setItem(row, 5, QTableWidgetItem(reserva["tipo_habitacion"]))
            table.setItem(row, 6, QTableWidgetItem("Sí" if reserva["mas_habitaciones"] else "No"))
            table.setItem(row, 7, QTableWidgetItem(reserva["cantidad_habitaciones"]))
            table.setItem(row, 8, QTableWidgetItem(reserva["huespedes"]))
            table.setItem(row, 9, QTableWidgetItem(reserva["forma_pago"]))

    def guardar_datos_csv(self):
        with open("datos_reservas.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            headers = ["Nombre", "Identificación", "Contacto", "Entrada", "Salida", "TipoHabitacion", "MasHabitaciones", "CantidadHabitaciones", "N° Huespedes", "FormaPago"]
            csvwriter.writerow(headers)
            for reserva in self.reservas_data:
                row = [
                    reserva["nombre"],
                    reserva["identificacion"],
                    reserva["contacto"],
                    reserva["entrada"],
                    reserva["salida"],
                    reserva["tipo_habitacion"],
                    "Sí" if reserva["mas_habitaciones"] else "No",
                    reserva["cantidad_habitaciones"],
                    reserva["huespedes"],
                    reserva["forma_pago"]
                ]
                csvwriter.writerow(row)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
