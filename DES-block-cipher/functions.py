
""" This function returns back the extension and the file name of an specific path """
def getFileExtension(file_path):
    snippets = file_path.split('/')[-1].split('.')
    fname = snippets[0]
    ext = snippets[1]
    return (fname, ext)

""" This function writes the cipher image as .bmp file """
def writeBMPFile( file_name, cipher_image, opm ):
    with open( f'encrypted-images/{file_name}_{opm}.bmp', 'wb' ) as file:
        file.write( cipher_image )

""" This function writes the decrypt image as .bmp file  """
def writeImageFile( file_name, decrypt_image ) :
    with open( f'decrypted-images/{file_name}.bmp', 'wb' ) as file:
        file.write( decrypt_image )

""" This function writes the Initialization Vector as .txt file """
def writeIVFile( iv ) :
    with open( 'iv.txt', 'wb' ) as file:
        file.write( iv )

""" This function writes the Initialization Vector as .txt file """
def readIVFile() :
    with open( 'iv.txt', 'rb' ) as file:
        iv = file.read()
    return iv

""" This function returns back BMP (Windows) Header"""
def getBMPHeader(file_name):
    with open( file_name, 'rb' ) as img:
        # Windows BMP files begin with a 54-byte header
        # Source: http://www.fastgraph.com/help/bmp_header_format.html
        image_header = img.read(54)

    return image_header

""" This function returns back the Image Content """
def getImgContent(file_name):
    with open( file_name, 'rb' ) as img:
        img.seek(54)
        # Reading the image content from byte 54
        image_content = img.read()
    
    return image_content