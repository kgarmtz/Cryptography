# Python Local Modules
from base64 import b64encode, b64decode
# Python Crypto Modules
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def encryptRSA( message ):
    key = RSA.import_key( open('private.pem').read() )
    h = SHA256.new( message )
    signature = pkcs1_15.new(key).sign(h)
    print(f'Original Signature: {signature}\n')
    return b64encode(signature)

def decryptRSA( signature, message ):
    key = RSA.import_key( open('public.pem').read() )
    h = SHA256.new( message )
    try:
        pkcs1_15.new(key).verify( h, signature )
        print('The signature is valid')
        return 1
    except (ValueError, TypeError):
        print('The signature is not valid')
        return 0
