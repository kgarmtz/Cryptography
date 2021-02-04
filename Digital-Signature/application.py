# Python Local Modules
import sys
import re
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
                message   = open('equipo.txt', 'rb').read()
                print(f'Message: {message}')
                signature = encryptRSA( message )
                with open( 'signed_equipo.txt', 'wb' ) as file:
                    # Embedding the signature into the file
                    file.write( message + b'\nSIGNATURE:' + signature )
                self.createMessageBox( 'Success', 'The file was successfully signed' )
            # Descifrado con el cifrador de clave pública RSA
            else:
                plaintext  = [ line.decode('utf-8') for line in open('signed_equipo.txt', 'rb').readlines() ]
                submessage = plaintext[:-1]
                # Removing the new line form the last line of the message
                lastline   = submessage[-1].rstrip('\n')
                submessage.pop(-1)
                submessage.append( lastline ) 
                message =  ''.join(submessage).encode('utf-8')
                print(f'Original Message: {message}')
                # Splitting up the signature from the message
                signature = b64decode( re.findall('SIGNATURE:(\S+)', plaintext[-1])[0] )
                print(f'Original Signature: {signature}')
                # Signature Verifying Process
                response = decryptRSA( signature, message )
                if response:
                    self.createMessageBox( 'Success!', 'The signature is valid' )
                else:
                    self.createMessageBox( 'Error!', 'The signature is not valid' )
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
