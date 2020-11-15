import sys
# Importamos la función uic para cargar la Interfaz Gráfica
from PyQt5 import uic
from PyQt5.QtCore import QDir

from PyQt5.QtWidgets import (
    QMainWindow,  # QMainWindow hace referencia a nuestra ventana principal
    QApplication, # QApplication se utiliza para cargar la aplicación
    QFileDialog,
    QMessageBox
)

# Abrimos nuestro archivo .ui
qtCreatorFile = "interface.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class NameApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
         # Si sobreescribimos clases de QMainWindow necesitamos inicializar sus respectivos constructores
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Establecemos un tamaño fijo de la pantalla con setFixedSize(width, height) 
        QMainWindow.setFixedSize(self, 716, 292)
         """ Buttons's Events """
        # self.btn_loadfile.clicked.connect(self.loadFiles)


    def createMessageBox(self, title, maintext):
        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle(title)
        box.setText(maintext)
        # Mostramos la caja de texto
        box.exec_()

# Cuando ejecutemos la app todo lo que esté aquí definido se ejecutará
if __name__ == '__main__':
    # Iniciamos la aplicación
    app = QApplication(sys.argv)
    # Inicializamos nuestra clase
    GUI = NameApp()
    # Mostramos nuestra aplicación
    GUI.show()
    # Cerramos nuestra aplicación
    sys.exit(app.exec_())
