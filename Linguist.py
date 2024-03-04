import csv
import os

def supported_langs_file():
    if os.path.exists("Tesseract_langs.txt"):
        return "Tesseract_langs.txt"
    else:
        print("The expected supported languages file is not in the directory.")
        return None

def get_language_from_code(code):
    file = supported_langs_file()   
    l_dict = {}
        
