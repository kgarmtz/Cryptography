# Local Python Modules
from base64 import b64encode, b64decode
# Crypto functions for Encrypt and Decrypt data
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
# Crypto functions for signature process
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def encryptAES( plaintext, aes_key ):
    # Defining the operation mode for AES 
    operation_mode = AES.MODE_CBC
    # Creating an instance of the cipher
    cipher = AES.new(aes_key, operation_mode)
    # Encrypting the data
    ciphertext_bytes = cipher.encrypt( pad(plaintext, AES.block_size) )
    # Getting the ciphertext as python base64 object (bytes)
    ciphertext = b64encode(ciphertext_bytes)
    print(f'ORIGINAL BYTES CIPHERTEXT: {ciphertext_bytes}\n')
    # Getting the initialization vector as python base64 object (bytes)
    iv = b64encode(cipher.iv)
    print(f'ORIGINAL BYTES IV: {cipher.iv}\n')
    
    return ciphertext, iv
    
def encryptKeyRSA( key ):
    # Retrieving the public key of my friend
    publickey = RSA.importKey( open('public.pem').read() )
    cipher = PKCS1_OAEP.new( publickey )
    # Encrypting it with RSA cipher
    cipherkey = cipher.encrypt( key )
    print(f'ORIGINAL BYTES RSA KEY: {cipherkey}\n')
    return b64encode(cipherkey)

def decryptKeyRSA( cipherkey ):
    try:
        # Retrieving my private key 
        privatekey = RSA.importKey( open('private.pem').read() )
        cipher = PKCS1_OAEP.new( privatekey )
        aes_key = cipher.decrypt( cipherkey )
        return aes_key
    
    except Exception as e:
        # Showing the exception 
        print( e )
        return 0
    
def decryptAES( ciphertext, aes_key, iv ):
    
    try:
        # Defining the operation mode for AES 
        operation_mode = AES.MODE_CBC
        # Creating an instance of the cipher
        cipher = AES.new(aes_key, operation_mode, iv=iv)
        # Retrieving the plaintext
        plaintext_bytes = unpad( cipher.decrypt(ciphertext) , AES.block_size)

        return plaintext_bytes
    
    except Exception as e:
        # Showing the exception 
        print( e )
        return 0
    
def signFile( plaintext ):
    # Loading my private key
    key = RSA.import_key( open('private.pem').read() )
    h = SHA256.new( plaintext )
    signature = pkcs1_15.new(key).sign(h)
    print(f'Original Signature: {signature}\n')
    return b64encode(signature)

def verifySign( signature, plaintext ):
    # Loading my friend public key
    key = RSA.import_key( open('candy.pem').read() )
    h = SHA256.new( plaintext )
    try:
        pkcs1_15.new(key).verify( h, signature )
        print('The signature is valid')
        return 1
    except (ValueError, TypeError):
        print('The signature is not valid')
        return 0
