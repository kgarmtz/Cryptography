# Importamos módulos locales de Python 
import sys
from base64 import b64encode, b64decode
# Importamos la función uic para cargar la Interfaz Gráfica
from PyQt5 import uic
from PyQt5.QtCore import QDir
# Importamos los widgets que vayamos a utilizar 
from PyQt5.QtWidgets import (
    QMainWindow,  # QMainWindow hace referencia a nuestra ventana principal
    QApplication, # QApplication se utiliza para cargar la aplicación
    QFileDialog,
    QMessageBox
)
# Importamos nuestras funciones locales
from functions import getFileExtension
from cipher import encryptRSA, decryptRSA

# Abrimos nuestro archivo .ui
qtCreatorFile = 'interface.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

path_file = ''

class RSACipher( QMainWindow, Ui_MainWindow ):
    def __init__( self ):
         # Si sobreescribimos clases de QMainWindow necesitamos inicializar sus respectivos constructores
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Establecemos un tamaño fijo de la pantalla con setFixedSize(width, height) 
        QMainWindow.setFixedSize(self, 415 , 433 )
        """ Buttons's Events """
        self.btn_loadfile.clicked.connect( self.loadFile )
        self.btn_start.clicked.connect( self.start )

    def loadFile( self ):
        file, _ = QFileDialog.getOpenFileName(self, 'Select a File', QDir.currentPath(), "Files (*.txt)")
        # Si el archivo existe
        if file:
            self.fname, self.ext = getFileExtension(file)
            self.txt_file.setText(f'{self.fname}.{self.ext}')
            # Guardamos la ruta del archivo seleccionado  
            global path_file  
            path_file = file

    def start( self ):
        # Función: Cifrar/Descifrar
        funct = self.cmb_function.currentIndex()
        # Si ya se selecciono un archivo
        if path_file:
            # Cifrado con el cifrador de clave pública RSA 
            if funct == 0:
                plaintext  = open('equipo.txt', 'rb').read()
                # publickey = self.txtPublicKey.toPlainText()
                ciphertext = encryptRSA( plaintext )
                with open( 'RSA-ciphertext.txt', 'w' ) as file:
                    file.write( b64encode(ciphertext).decode('utf-8')  )
                self.createMessageBox( 'Success', 'The plaintext was successfully encrypted' )
            # Descifrado con el cifrador de clave pública RSA
            else:
                ciphertext = b64decode( open('RSA-ciphertext.txt', 'r').read() )
                plaintext  = decryptRSA( ciphertext )
                if plaintext is not None:
                    print(f'Decrypted text:\n {plaintext}' )
                    with open( 'RSA-plaintext.txt', 'w') as file:
                        file.write( plaintext )
                    self.createMessageBox( 'Success', 'The ciphertext was successfully decrypted' )
                else:
                    self.createMessageBox( 'Error', 'Something went wrong in decryption process ...' )
        else:
            self.createMessageBox('Error!', 'You must select a textfile')


    def createMessageBox( self, title, maintext ):
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
    GUI = RSACipher()
    # Mostramos nuestra aplicación
    GUI.show()
    # Cerramos nuestra aplicación
    sys.exit(app.exec_())
