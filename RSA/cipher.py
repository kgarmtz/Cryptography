from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def encryptRSA( plaintext ):
    
    publickey = RSA.importKey( open('public.pem').read() )
    cipher = PKCS1_OAEP.new( publickey )
    ciphertext = cipher.encrypt( plaintext )
    return ciphertext

def decryptRSA( ciphertext ):
    
    try:
        privatekey = RSA.importKey( open('private.pem').read() )
        cipher = PKCS1_OAEP.new( privatekey )
        plaintex = cipher.decrypt( ciphertext )
        return plaintex.decode('utf-8')
    
    except Exception as e:
        # Mostramos la excepción 
        print( e )
    
