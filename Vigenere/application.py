import sys
import random
from string import ascii_lowercase
# Importamos nuestras funciones locales
from functions import *
# Importamos la función uic para cargar la Interfaz Gráfica
from PyQt5 import uic
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

class CiphersAffineVigenere(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        # Si sobreescribimos clases de QMainWindow estás a su vez se inicializarán
        QMainWindow.__init__(self)
        # Establecemos un tamaño fijo de la pantalla con setFixedSize(width, height) 
        QMainWindow.setFixedSize(self, 761,478)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        """ QtWidgets Design """
        # Hiding the components of Affine and Vigenere Cipher
        self.showWidgets(False, False)
        """ Buttons's Events """
        self.btn_loadfile.clicked.connect(self.loadFiles)
        self.btn_random_aff.clicked.connect(self.getRandomKeyAff)
        self.btn_random_vig.clicked.connect(self.getRandomKeyVig)
        self.btn_start.clicked.connect(self.start)
        # adding action to combo box
        self.cmb_cipher.activated.connect(self.comboFunction) 

    def showWidgets(self, aff, vig, cmb_cipher=True):
        # Affine Components
        self.btn_random_aff.setVisible(aff)
        self.lbl_info_7.setVisible(aff)
        self.lbl_info_8.setVisible(aff)
        self.txtAlpha.setVisible(aff)
        self.txtBeta.setVisible(aff)
        # Vigenere Components
        self.txtkey.setVisible(vig)
        self.btn_random_vig.setVisible(vig)
        self.lbl_info_9.setVisible(vig)
        # ComboBox Cipher
        self.cmb_cipher.setEnabled(cmb_cipher)

    def comboFunction(self):
        # 1: Affine 
        if self.cmb_cipher.currentIndex() == 1:
            self.showWidgets(True, False)
            self.txtAlphabet.setText(' ')
            self.txtAlphabet.setEnabled(True)
            
        # 2: Vigenere
        elif self.cmb_cipher.currentIndex() == 2:
            self.showWidgets(False, True)
            # Solamente se cifrará con modulo 26 (26 characteres for the English Alphabet )
            self.txtAlphabet.setText('26')
            self.txtAlphabet.setEnabled(False)
    
    def loadFiles(self):
        self.txtOutput.clear()
        file, _ = QFileDialog.getOpenFileName(self, 'Select a File', QDir.currentPath(), "Text Files (*.txt)")
        # Si el archivo existe
        if file:
            self.fname, self.ext = getFileExtension(file)
            self.txt_file.setText(f'{self.fname}.{self.ext}')
            # Guardamos la ruta del archivo seleccionado  
            self.path_file = file
            # Reading the content of the chosen file
            self.text = open( self.path_file, 'r', encoding='utf-8').read()
            self.txtInput.setText(self.text)
            # Validating the file extension
            if self.ext == 'aff':
                self.cmb_cipher.setCurrentIndex(1)
                self.showWidgets(True, False, False)
                self.cmb_function.setCurrentIndex(1)

            elif self.ext == 'vig':
                self.cmb_cipher.setCurrentIndex(2)
                self.showWidgets(False, True, False)
                self.cmb_function.setCurrentIndex(1)
            else:
                self.cmb_cipher.setCurrentIndex(0)
                self.showWidgets(False, False)
            
    def getRandomKeyAff(self):
        if self.txtAlphabet.toPlainText() != '':
            n = int(self.txtAlphabet.toPlainText())
            # Generating alpha and beta randomly
            a = 0
            b = random.randrange(1,n+1) # 1<=b<=n
            validation = False
            while( not validation ):
                a = random.randrange( 1, n ) # 1<=a<n
                validation = validateKey( a, n )
            # Showing the values in the text area
            self.txtAlpha.setText( str(a) )
            self.txtBeta.setText( str(b) )

        else:
            self.createMessageBox("Error!", f"You must give the alphabet length")

    def getRandomKeyVig(self):
        if self.txt_file.toPlainText() != '':
            key = []
            # Putting all the characters together 
            texto = "".join( char for char in self.text if char!='\n' and char!=' ')
            for _ in range(len(texto)):
                key.append(random.choice(list(ascii_lowercase)))
            self.txtkey.setText("".join(key))

        else:
             self.createMessageBox("Error!", f"You must select a file text to Encrypt")

    def start(self):
        self.n = int(self.txtAlphabet.toPlainText()) 
        # If 26 modulus is provided...
        self.extra = 97 if self.n == 26 else 0
        # If 97 modulus is provided... 
        if (self.n == 97):
            self.text = self.text.upper()
            print(self.text)

        # 1: Affine 2: Vigenere
        cipher = self.cmb_cipher.currentIndex()
        # If there is no cipher selected
        if cipher == 0:
            self.createMessageBox("Error!", f"You must select a cipher")
        # 0: Encrypt 1: Decrypt
        function = self.cmb_function.currentIndex()
        # Encrypt
        if function == 0:
            # Affine
            if cipher == 1:
                # original values
                self.a = int(self.txtAlpha.toPlainText())
                self.b = int(self.txtBeta.toPlainText())
                # Validating alpha for the modulus n
                if validateKey(self.a,self.n):
                    self.createMessageBox("Good Job!", f"The key 'a': {self.a} is correct for n = {self.n} ")  
                    # Creating the key for the Affine Cipher
                    key = {'a':self.a, 'b':self.b, 'n':self.n}
                    cipherText = encryptAffine( self.text , key )
                    self.txtOutput.setText(cipherText)
                    # Dumping the ciphertext into a file
                    writeFile(f'{self.fname}.aff', cipherText)
                else:
                    self.createMessageBox("Error!", f"Invalid key 'a': {self.a} is provided. Remainder: gcd({self.a},{self.n}) must be equal to 1 ")  

            # Vigenere
            elif cipher == 2:
                # Putting all the characters together 
                self.text = "".join( char for char in self.text if char!='\n' and char!=' ')
                # Creating the key for the Vigenere Cipher
                self.keyVig = adjustKey( len(self.text), self.txtkey.toPlainText())
                self.keyVig = "".join( chr(ord(char)-self.extra) for char in self.keyVig )
                plainText = "".join( chr(ord(char)-self.extra) for char in self.text )
                key = {'key':self.keyVig, 'n':self.n, 'x':self.extra}
                cipherText = encryptVigenere( plainText , key )
                self.txtOutput.setText( cipherText )
                # Dumping the ciphertext into a file
                writeFile(f'{self.fname}.vig', cipherText)

        # Decrypt
        else:
            # Performing decrypt function for affine cipher
            if cipher == 1:
                # original values
                self.a = int(self.txtAlpha.toPlainText())
                self.b = int(self.txtBeta.toPlainText())
                # Computing the inverse of 'a' regarding 'n'
                inverse_a = inverse( self.a, self.n )
                print(f"The inverse of a: {self.a} is a^-1: {inverse_a} ")
                # Computing the additive inverse of 'b' regarding 'n'
                add_inv_b = addInverse( self.b, self.n )
                key = {'a-1':inverse_a, 'b-1':add_inv_b, 'n':self.n}
                plainText = decryptAffine( self.text, key )
                self.txtOutput.setText(plainText)

            # Performing decrypt function for Vigenere cipher
            elif cipher == 2:
                # Putting all the characters together 
                self.text = "".join( char for char in self.text if char!='\n' and char!=' ')
                # Creating the key for the Vigenere Cipher
                self.keyVig = adjustKey( len(self.text), self.txtkey.toPlainText())
                self.keyVig = "".join( chr(ord(char)-self.extra) for char in self.keyVig )
                cipherText = "".join( chr(ord(char)-self.extra) for char in self.text )
                key = {'key':self.keyVig, 'n':self.n, 'x':self.extra}
                plainText = decryptVigenere( cipherText , key )
                self.txtOutput.setText(plainText)

    def createMessageBox(self, title, maintext):
        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle(title)
        box.setText(maintext)
        # Showing the message box
        box.exec_()


# Cuando ejecutemos la app todo lo que esté aquí definido se ejecutará
if __name__ == '__main__':
    # Iniciamos la aplicación
    app = QApplication(sys.argv)
    # Inicializamos nuestra clase
    GUI = CiphersAffineVigenere()
    # Mostramos nuestra aplicación
    GUI.show()
    # Cerramos nuestra aplicación
    sys.exit(app.exec_())
