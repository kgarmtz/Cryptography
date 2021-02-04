""" This function returns back the extension and the file name of an specific path """
def getFileExtension( file_path ):
    snippets = file_path.split('/')[-1].split('.')
    fname = snippets[0]
    ext = snippets[1]
    return (fname, ext)
