""" This function returns back the extension and the file name of an specific path """
def getFileExtension(file_path):
    snippets = file_path.split('/')[-1].split('.')
    fname = snippets[0]
    ext = snippets[1]
    return (fname, ext)
    
""" This function returns back the greatest common divisor between two numbers """
def gcd(a,b):
    a,b = getMaximum(a,b)
    while b!=0:
        r = a%b
        a = b
        b = r
    return a

""" This function returns back the Bezout Coefficients performing the Extended Euclidean Algorithm """
# If a and b are positive integers, there exist integers unique non-negative q and r so that:
# a = (b)(q) + r, where q = quotient and r = remainder => r = a - (q)(b)
def xgcd(a,b):
    x,y = a,b
    # If a and b are different from zero, then: gcd(a,b) = a*u + b*v
    # gcd(a,0) = a = (a)(1) + 0 
    u0 = 1
    v0 = 0
    # gcd(0,b) = b = 0 + (b)(1)
    u1 = 0
    v1 = 1
    while(b!=0): 
        # q = a/b 
        q = a//b
        # r = a - (q)b 
        r = a - (q*b)
        # ui = (ui-2) - (q)(ui-1) = u0 - (q)(u1)
        u = u0 - (q*u1)
        # vi = (vi-2) - (q)(vi-1) = v0 - (q)(v1)
        v = v0 - (q*v1)
        # update the values of a, b for the next iteration
        a = b
        b = r
        # update the Bezout coefficients for the next iteracion
        u0 = u1
        v0 = v1
        u1 = u
        v1 = v
    return {x:u0,y:v0}

""" This function returns true if 'a' is a valid key for the affine cipher """
def validateKey(a,n):
    return True if gcd(a,n) == 1 else False

""" This function find the inverse of a number mod n for the affine cipher """
def inverse(a,n): 
     _a,_n = getMaximum(a,n)
     return validateInverse(xgcd(_a,_n)[a], n)

""" This function turns out a negative inverse of 'a' to postive value """
def validateInverse( inverse, mod ):
    if inverse > 0:
        return inverse
    else:
        i = 1
        aux = inverse
        while aux<0:
            aux = inverse + (i*mod)
            i+=1
        return aux

""" This function returns 'a' if it is greater than n, in otherwise 'n' """
def getMaximum( a, b):
    return (a,b) if a>b else (b,a)
    
""" This function implements the Affine cipher and returns the plaintext into cipher text """
def encryptAffine(plainText, key):
    cipherText = []
    a,b,n = key.values()
    for p in plainText:
        c = ( (a * ord(p)) + b ) % n
        cipherText.append( chr(c) )
    return "".join(cipherText)

""" This function implements the decrypt function for the Affine Cipher and returns the original plaintext """
def decryptAffine(cipherText, key):
    plainText = []
    n = key['n']
    # Reducing the expression for decryp function
    b = reduceAdditiveInverse(key['a-1'], key['b-1'], n)
    for c in cipherText:
        p = ( (key['a-1']*ord(c)) + b) % n 
        plainText.append( chr(p) ) 

    return "".join(plainText)

""" This function implements the Vigenere cipher and returns the plaintext into cipher text """
def encryptVigenere(plainText, key):
    cipherText = []
    n = key['n']
    x = key['x'] 

    for (p,k) in list(zip(plainText, key['key'])):
        c = ( ord(p) + ord(k) ) % n 
        cipherText.append( chr(c+x) )

    return "".join(cipherText)

""" This function implements the decrypt function for the Vigenere Cipher and returns the original plaintext """
def decryptVigenere(cipherText, _key):
    plainText = []
    n = _key['n']
    # Shifting + 97
    x = _key['x']
    # Computing the key for decrypt function
    key = additiveInverseVig(_key['key'], n)

    for (c,k) in list(zip(cipherText, key)):
        p = ( ord(c) + ord(k) ) % n 
        plainText.append(chr(p+x))

    return "".join(plainText)

""" This function writes the cipher text in a text file """
def writeFile(file_name, ciphertext):
    with open(f'{file_name}.txt', 'w', encoding='utf-8') as f:
        f.write(ciphertext)

""" This function returns the additive inverse of b regarding n for the Affine Cipher """
def addInverse(b, n):
    return n-b if n>b else validateInverse(-b,n)

""" This function returns the additive inverse of the key regarding n for the Vigenére Cipher """
def additiveInverseVig(key, n):
    # Additive inverse of every single character from the provided key 
    addKey = []
    for k in key:
        addKey.append( chr( n-ord(k) if n>ord(k) else validateInverse(-ord(k),n) ) )
    return "".join(addKey)

""" This function returns a simplified expression for b*n in order to simplify the decrypt function """
def reduceAdditiveInverse(a, b, n):
    return (a*b) % n

""" This function adjusts the key provided by the user """
def adjustKey( lon, key ):
    if lon == len(key):
        return key
    else:
        snippet = lon//len(key)
        r = lon%len(key)
        return key*snippet if r==0 else f'{key*snippet}{key[:r]}'  


