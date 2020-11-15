# Importamos nuestras funciones locales
from functions import *
# Importamos el cifrador simétrico de bloque DES
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

""" Implementación del Cifrado DES con distintos modos de operación
    Parámetros: 
        - image: Contenido de la Imagen
        -   key: Llave para cifrar, debe de ser de un tamaño fijo de 8 bytes 
        -   opm: Modo de Operación que será utilizado para el cifrado
"""

def encryptDES( image, key, opm ):
    operation_mode = [ DES.MODE_ECB, DES.MODE_CBC, DES.MODE_CFB, DES.MODE_OFB ]
    mode_extension = [ 'ecb', 'cbc', 'cfb', 'ofb']
    encrypted_img_bytes = b''
    
    # Definimos el modo de operación del Cifrador de Bloque DES
    cipher = DES.new( key, operation_mode[opm] )

    # Cifrado con Modo de Operación: ECB
    if opm == 0:
        # Ajustamos el tamaño de los datos para que sea múltiplo del tamaño de bloque del cifrador DES 
        encrypted_img_bytes = cipher.encrypt( pad( image, DES.block_size ) )
    
    # Cifrado con Modo de Operación: CBC
    elif opm == 1:
        # El Vector de Inicialización es una secuencia de bytes del mismo tamaño de bloque del cifrador DES
        writeIVFile( cipher.iv )
        # Ajustamos el tamaño de los datos para que sea múltiplo del tamaño de bloque del cifrador DES 
        encrypted_img_bytes = cipher.encrypt( pad( image, DES.block_size ) )

    # Cifrado con los siguientes Modos de Operación: CFB, OFB
    else:
        # Escribimos el Vector de Inicialización usado para el cifrado
        writeIVFile( cipher.iv )
        # Aplicamos la función de cifrado, ya que CBF y OFB reciben datos de cualquier longitud
        encrypted_img_bytes = cipher.encrypt( image )

    # Retornamos la imagen cifrada 
    return ( encrypted_img_bytes, mode_extension[opm] ) 
        


""" Implementación del Descifrado DES con distintos modos de operación
    Parámetros: 
        - image: Contenido de la Imagen
        -   key: Llave para cifrar, debe de ser de un tamaño fijo de 8 bytes
        -   opm: Modo de Operación que será utilizado para el descifrado
        -    iv: Vector de Inicialización, por defecto es 'None' 
"""

def decryptDES( encrypted_image, key, opm, iv = None ):
    operation_mode = [ DES.MODE_ECB, DES.MODE_CBC, DES.MODE_CFB, DES.MODE_OFB ]
    img_bytes = b''

    # Descifrado con Modo de Operación: ECB
    if opm == 0:
        # Definimos el modo de operación del Cifrador de Bloque DES
        cipher = DES.new( key, operation_mode[opm] )
        # Aplicamos la función de descifrado 
        img_bytes = unpad( cipher.decrypt( encrypted_image ), DES.block_size)

    # Descifrado con Modo de Operación: CBC
    elif opm == 1:
        # Definimos el modo de operación del Cifrador de Bloque DES
        cipher = DES.new( key, operation_mode[opm], iv )
        # Aplicamos la función de descifrado 
        img_bytes = unpad( cipher.decrypt( encrypted_image ), DES.block_size)

    # Descifrado con los siguientes Modos de Operación: CFB, OFB
    else: 
        # Definimos el modo de operación del Cifrador de Bloque DES
        cipher = DES.new( key, operation_mode[opm], iv )
        # Aplicamos la función de descifrado, ya que CBF y OFB reciben datos de cualquier longitud
        img_bytes = cipher.decrypt( encrypted_image )

    # Retornamos la imagen descifrada 
    return img_bytes


    