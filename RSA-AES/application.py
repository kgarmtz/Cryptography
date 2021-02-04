# Importamos módulos locales de Python 
import sys, re
from base64 import b64encode, b64decode
# Importamos la función uic para cargar la Interfaz Gráfica
from PyQt5 import uic
from PyQt5.QtCore import QDir
from Crypto.Random import get_random_bytes
# Importamos los widgets que vayamos a utilizar 
from PyQt5.QtWidgets import (
    QMainWindow,  # QMainWindow hace referencia a nuestra ventana principal
    QApplication, # QApplication se utiliza para cargar la aplicación
    QFileDialog,
    QMessageBox
)
# Importamos nuestras funciones locales
from functions import (
    getFileExtension,
    separateSignatureFromText,
)

from cipher import (
    encryptKeyRSA, 
    decryptKeyRSA, 
    encryptAES, 
    decryptAES,
    signFile,
    verifySign
)

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
        QMainWindow.setFixedSize(self, 540, 364 )
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
        # Function: Encrypt/Decrypt
        funct   = self.cmb_function.currentIndex()
        # Digital Signature Service: Enable/Disable
        service = self.cmb_signature.currentIndex()

        # If there is a selected file 
        if path_file:
            if not funct and not service:
                self.createMessageBox('Error!', 'Please, select one option to execute...')
            # Encrypting with AES and RSA 
            elif funct == 1 and service!=1 and service!=2:
                print('---- ENCRYPT PROCESS ----\n')
                plaintext  = open(path_file, 'rb').read()
                # Generating the random key for AES cipher (16 bytes = 128 bits long)
                aes_key = get_random_bytes(16)
                print(f'ORIGINAL BYTES AES KEY: {aes_key}\n')
                ciphertext, iv = encryptAES( plaintext, aes_key )
                # Encrypting the random key with RSA cipher and the public key
                cipherkey = encryptKeyRSA( aes_key )
                # Writing the ciphertext, cipherkey and the initialization vector in the same file 'encrypted'
                with open('encrypted.txt', 'wb') as file:
                    file.write( ciphertext + b'\nAES-IV:' + iv + b'\nRSA-KEY:' + cipherkey )
                    self.createMessageBox('Success!', 'The file was encrypted successfully')
            # Decrypting with AES and RSA
            elif funct == 2 and service!=1 and service!=2:
                print('---- DECRYPT PROCESS ----\n')
                data = [ line.decode('utf-8') for line in open(path_file, 'rb').readlines() ]
                ciphertext_bytes = b64decode( data[0] )
                print(f'ORIGINAL BYTES CIPHERTEXT: {ciphertext_bytes}\n')
                iv_bytes = b64decode( re.findall('AES-IV:(\S+)' , data[1])[0] )
                print(f'ORIGINAL BYTES IV: {iv_bytes}\n')
                rsa_key_bytes = b64decode( re.findall('RSA-KEY:(\S+)' , data[2])[0] )  
                print(f'ORIGINAL BYTES RSA KEY: {rsa_key_bytes}\n')
                aes_key = decryptKeyRSA( rsa_key_bytes )
                if aes_key != 0:
                    print(f'ORIGINAL BYTES AES KEY: {aes_key}\n')
                else:
                    self.createMessageBox('Error!', 'Something went wrong in the RSA decryption process')
                
                plaintext_bytes = decryptAES( ciphertext_bytes, aes_key, iv_bytes )
                if plaintext_bytes != 0:
                    with open('decrypted.txt', 'wb') as file:
                        file.write( plaintext_bytes )
                        self.createMessageBox('Success!', 'The file was decrypted successfully')
                else:
                    self.createMessageBox('Error!', 'Something went wrong in the AES decryption process')

            elif service == 1 and funct!=1 and funct!=2:
                print('Digital signature service was activated as sign')
                message   = open(path_file, 'rb').read()
                signature = signFile( message )
                with open( 'signed.txt', 'wb' ) as file:
                    # Embedding the signature into the file
                    file.write( message + b'\nSIGNATURE:' + signature )
                self.createMessageBox( 'Success', 'The file was successfully signed' )
            
            elif service == 2 and funct!=1 and funct!=2:
                print('Digital signature service was activated as verify')
                # Separating the message from the signature
                message, signature = separateSignatureFromText( path_file )
                # Signature Verifying Process
                response = verifySign( signature, message )
                if response:
                    self.createMessageBox( 'Success!', 'The signature is valid' )
                else:
                    self.createMessageBox( 'Error!', 'The signature is not valid' )

            elif service == 1 and funct == 1:
                print('Both services were activated as encrypt and sign')
                plaintext  = open(path_file, 'rb').read()
                # Generating a random aes key
                aes_key = get_random_bytes(16)
                # Encrypting the plaintext and retrieving the AES key
                ciphertext, iv = encryptAES( plaintext, aes_key )
                # Encrypting the AES key
                cipherkey = encryptKeyRSA( aes_key )
                # Signing the file
                signature = signFile( plaintext )
                # Writing the ciphertext, cipherkey, the initialization vector and the signature in the same file 'encrypted'
                with open('encrypted-signed.txt', 'wb') as file:
                    file.write( ciphertext + b'\nAES-IV:' + iv + b'\nRSA-KEY:' + cipherkey + b'\nSIGNATURE:' + signature )
                    self.createMessageBox('Success!', 'The file was encrypted and signed successfully')

            elif service == 2 and funct == 2:
                print('Both services were activated as decrypt and verify')
                # Retrieving the ciphertext from the whole file
                data = [ line.decode('utf-8') for line in open(path_file, 'rb').readlines() ]
                ciphertext_bytes = b64decode( data[0] )
                # Retrieving the initialization vector
                iv_bytes = b64decode( re.findall('AES-IV:(\S+)' , data[1])[0] )
                # Retrieving the encrypted AES key
                rsa_key_bytes   = b64decode( re.findall('RSA-KEY:(\S+)' , data[2])[0] )
                # Retrieving the signature for the verifying process
                signature_bytes = b64decode( re.findall('SIGNATURE:(\S+)' , data[3])[0] )
                # Decrypting the AES key with RSA
                aes_key = decryptKeyRSA( rsa_key_bytes )
                if not aes_key:
                    self.createMessageBox('Error!', 'Something went wrong in the AES-key decryption process')
                # Decrypting the file with the decrypted AES key
                plaintext_bytes = decryptAES( ciphertext_bytes, aes_key, iv_bytes )
                # If the plaintext was not retrieved successfully
                if not plaintext_bytes:
                    self.createMessageBox('Error!', 'Something went wrong in the ciphertext decryption process')
                # If the plaintext was retrieved successfully
                else:
                    with open('decrypted-verified.txt', 'wb') as file:
                        file.write( plaintext_bytes )
                    # Signature Verifying Process
                    response = verifySign( signature_bytes, plaintext_bytes )
                    # If everything went ok
                    if response :
                        self.createMessageBox('Success!', 'The file was decrypted and the signature was verified successfully')
                    else:
                        self.createMessageBox('Error!', 'Something went wrong with the sign verification process')

            else:
                self.createMessageBox('Error!', 'Not match, try again :(')
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
