from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class VerticalToolbarExample(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear la barra de herramientas vertical
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Agregar acciones a la barra de herramientas
        self.action1 = QAction("Acción 1", self)
        self.action2 = QAction("Acción 2", self)
        self.action3 = QAction("Acción 3", self)
        self.toolbar.addAction(self.action1)
        self.toolbar.addAction(self.action2)
        self.toolbar.addAction(self.action3)

        # Crear el diseño principal y agregar la barra de herramientas
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # Establecer el diseño vertical de la barra de herramientas
        self.toolbar.setOrientation(Qt.Vertical)
        
        # Agregar la barra de herramientas al layout principal alineada a la derecha
        layout.addWidget(self.toolbar, alignment=Qt.AlignRight)

if __name__ == '__main__':
    app = QApplication([])
    window = VerticalToolbarExample()
    window.show()
    app.exec()
