from smart_open import open

def read_file(path):
    """
    Take file path extract text and return text.
    """
    with open(path, 'r') as infile:
        text = infile.read() 
    return text