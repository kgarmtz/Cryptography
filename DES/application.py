import sys
# Importamos la función uic para cargar la Interfaz Gráfica
from PyQt5 import uic
from PyQt5.QtCore import QDir
# Importamos nuestras funciones locales
from functions import *
from cipher_functions import *

from PyQt5.QtWidgets import (
    QMainWindow,  # QMainWindow hace referencia a nuestra ventana principal
    QApplication, # QApplication se utiliza para cargar la aplicación
    QFileDialog,
    QMessageBox
)

# Abrimos nuestro archivo .ui
qtCreatorFile = 'interface.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Variables globales 
path_file = ''

class cypherDESApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
         # Si sobreescribimos clases de QMainWindow necesitamos inicializar sus respectivos constructores
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Establecemos un tamaño fijo de la pantalla con setFixedSize(width, height) 
        QMainWindow.setFixedSize(self, 716, 292)
        """ Buttons's Events """
        self.btn_loadfile.clicked.connect(self.loadFiles)
        self.btn_start.clicked.connect(self.start)

    def loadFiles(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select a File', QDir.currentPath(), "Images (*.bmp)")
        # Si el archivo existe
        if file:
            self.fname, self.ext = getFileExtension(file)
            self.txt_file.setText(f'{self.fname}.{self.ext}')
            # Guardamos la ruta del archivo seleccionado  
            global path_file  
            path_file = file
            # Validamos la terminación del archivo
            if self.fname.endswith('ecb'):
                self.comboBoxOptions( 1, 0 )
            elif self.fname.endswith('cbc'):
                self.comboBoxOptions( 1, 1 )
            elif self.fname.endswith('cfb'):
                self.comboBoxOptions( 1, 2 )
            elif self.fname.endswith('ofb'):
                self.comboBoxOptions( 1, 3 )
            else:
                self.comboBoxOptions( 0, 0 )

    def start(self): 
        # Obtenemos las opciones seleccionadas por el usuario
        plainKey = self.txtKey.toPlainText()

        if path_file and len(plainKey) == 8:
            
            # Unicode -> Bytes 
            key = plainKey.encode('utf-8')
            # Modo de Operación
            opm = self.cmb_operation.currentIndex()
            # Función: Cifrar/Descifrar
            funct = self.cmb_function.currentIndex()
            # Leemos el encabezado de 54 bytes para Windows
            image_header = getBMPHeader( path_file )
            # Leemos el contenido de la imagen 
            image_content = getImgContent( path_file )

            # Cifrado con el cifrador de Bloque DES 
            if funct == 0:
                # Ciframos el contenido de la imagen
                encrypted_image, mode_ext = encryptDES( image_content, key, opm )    
                # Construimos la imagen con el encabezado y el contenido cifrado
                image = image_header + encrypted_image 
                writeBMPFile( self.fname, image, mode_ext )
                self.createMessageBox('Success!', 'The image was encrypted successfully')
            
            # Descifrado con el cifrador de Bloque DES 
            elif funct == 1:
                # Modo de operación: EBC
                if opm == 0:
                    # Desciframos el contenido de la imagen
                    decrypted_image = decryptDES( image_content, key, opm)
                    # Validamos si el modo de operación es el correcto
                    if decrypted_image == 1:
                        self.createMessageBox('Error!', 'Bad Operation Mode Selected')
                    else:
                        # Construimos la imagen con el encabezado y el contenido cifrado
                        image = image_header + decrypted_image 
                        writeImageFile( self.fname, image )  
                        self.createMessageBox('Success!', 'The encrypted image was decrypted successfully')
                        
                # Modos de operación: CBC, CFB, OFB 
                else:
                    # Obtenemos el Vector de Inicialización 
                    iv = readIVFile()
                    # Desciframos el contenido de la imagen
                    decrypted_image = decryptDES( image_content, key, opm, iv)
                    # Validamos si el modo de operación es el correcto
                    if decrypted_image == 1:
                        self.createMessageBox('Error!', 'Bad Operation Mode Selected')
                    else:
                        # Construimos la imagen con el encabezado y el contenido cifrado
                        image = image_header + decrypted_image 
                        writeImageFile( self.fname, image )  
                        self.createMessageBox('Success!', 'The encrypted image was decrypted successfully')

        else:
            self.createMessageBox("Error!", f"You must select an image and provide a key of eight characters length")

    def comboBoxOptions(self, function, op_mode):
        # function corresponde al combo box de función cifrar/descifrar
        self.cmb_function.setCurrentIndex(function)
        # op_mode corresponde al modo de operación 
        self.cmb_operation.setCurrentIndex(op_mode)

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
    GUI = cypherDESApp()
    # Mostramos nuestra aplicación
    GUI.show()
    # Cerramos nuestra aplicación
    sys.exit(app.exec_())
