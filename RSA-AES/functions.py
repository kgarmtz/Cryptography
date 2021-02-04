import re
from base64 import b64encode, b64decode

""" This function returns back the extension and the file name of an specific path """
def getFileExtension( file_path ):
    snippets = file_path.split('/')[-1].split('.')
    fname = snippets[0]
    ext = snippets[1]
    return (fname, ext)

""" This function separates the message from the signature """
def separateSignatureFromText( path_file ):
    plaintext  = [ line.decode('utf-8') for line in open(path_file, 'rb').readlines() ]
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
    
    return (message, signature) 
