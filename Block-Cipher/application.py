import sys, json
# Importamos el cifrador simétrico DES
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
# Importamos la función uic para cargar la Interfaz Gráfica
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDir
# QMainWindow hace referencia a nuestra ventana principal
# QApplication se utiliza para cargar la aplicación
from PyQt5.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QFileDialog,
    QMessageBox
)


# Abrimos nuestro archivo .ui
qtCreatorFile = "interface.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
# Archivo Local 
path_file = ""
file_name = ""

class cypherApp(QMainWindow, Ui_MainWindow):

    def __init__(self):
        # Si sobreescribimos clases de QMainWindow estás a su vez se inicializarán
        QMainWindow.__init__(self)
        # Establecemos un tamaño fijo de la pantalla con setFixedSize(width, height) 
        QMainWindow.setFixedSize(self, 483,440)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        """ Diseño de los QtWidgets """
        font = QFont()
        font.setBold(True)
        self.btn_loadfile.setFont(font)
        self.btn_encrypt.setEnabled(False)
        self.btn_decrypt.setEnabled(False)
        """ Buttons's Events """
        self.btn_loadfile.clicked.connect(self.load_files)
        self.btn_encrypt.clicked.connect(self.encrypt_file)
        self.btn_decrypt.clicked.connect(self.decrypt_file)
        
    
    # Función para cargar el archivo a cifrar
    def load_files(self):
        # Solamente se permitirá elegir archivos .txt y .json All Files (*)
        file, _ = QFileDialog.getOpenFileName(self, 'Select a File', QDir.currentPath(), "JSON files (*.json);;Text Files (*.txt)")
        if file:
            chunks = file.split('/')
            self.txt_file.setText(chunks[-1])
            extension = chunks[-1].split('.')
            # Guardamos la ruta del archivo seleccionado
            global path_file  
            path_file = file
            # Validamos el tipo de extensión
            if extension[1] == 'txt':
                global file_name
                file_name = extension[0]
                self.btn_encrypt.setEnabled(True)
            elif extension[1] == 'json':
                self.btn_decrypt.setEnabled(True)
                
    # Función para cifrar el archivo
    def encrypt_file(self):
        # Abrimos el archivo
        file = open(path_file, 'r')
        # Obtenemos el contenido del archivo y lo convertimos a bytes
        plaintext = bytes( file.read() , encoding = 'utf-8' )
        # Cerramos el archivo
        file.close()
        # Esquema del Cifrador de Bloque DES
        key = get_random_bytes(8)
        # Definimos el modo de operación del Cifrador de Bloque DES
        cipher = DES.new(key, DES.MODE_CBC)
        # Ajustamos el tamaño de los datos para que este sea múltiplo del 
        # tamaño de bloque del cifrador de bloque (DES) y ciframos. 
        ct_bytes = cipher.encrypt(pad(plaintext, DES.block_size))
        # Como DES devuelve un 'cyphertext' que puede contener bytes que no se puedan leer 
        # por lo que lo codificamos en formato Base64 para convertir los datos binarios en 
        # carácteres ASCII. Una vez teniendo los carácteres ASCII, lo decodificamos en formato 
        # 'utf-8 Unicode' para obtener la apropiada representación de ciphertext como una cadena 'str' de Python
        # y lo podamos ingresar en el archivo JSON, ya que sí lo dejamos como bytes, estos no podran
        # seliarizarse dentro de este
        ct = b64encode(ct_bytes).decode('utf-8')
        # Obtenemos la interpretación del Vector de Inicialización como una cadena de Python 'str'
        iv = b64encode(cipher.iv).decode('utf-8')
        k  = b64encode(key).decode('utf-8')
        # Creamos un archivo json con el ciphertext obtenido y el Vector de Inicialización
        with open(f'{file_name}_C.json', 'w') as file:
            # json.dump escribe un objeto de Python en un archivo .json
            json.dump({'iv':iv, 'ciphertext':ct, 'key':k}, file, indent=4)
        self.createMessageBox("Success!", "Ciphertext File Created!") 
        self.btn_encrypt.setEnabled(False)
        self.txt_file.clear()

    def decrypt_file(self):
        try:
            # Obtenemos el contenido del archivo JSON que se encuentra en formato 64encode
            json_file = open(f'{self.txt_file.toPlainText()}', 'r')
            content = json_file.read()
            b64 = json.loads(content)
            json_file.close()
            # Decodificamos el contenido en formato Base64 en bytes de datos no codificados
            iv =  b64decode(b64['iv'])
            ct =  b64decode(b64['ciphertext'])
            key = b64decode(b64['key'])
            cipher = DES.new(key, DES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ct), DES.block_size).decode('utf-8')
            with open(f'{file_name}_D.txt', 'w') as file:
                file.write(plaintext)
            self.btn_decrypt.setEnabled(False)
            self.txt_file.clear()
            self.createMessageBox("Success!", "The Ciphertext was decrypted!") 
        except (ValueError, KeyError):
            print("Incorrect decryption")

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
    GUI = cypherApp()
    # Mostramos nuestra aplicación
    GUI.show()
    # Cerramos nuestra aplicación
    sys.exit(app.exec_())
