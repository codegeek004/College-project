import argparse
import os
import OCR 
import Linguist

def main():
    """
    Handles command line arguments and begins the real-time OCR by calling ocr_stream().A path to the Tesseract cmd root is required, but all other params areoptional.

    Example command-line use: python3 Main.py -t /usr/local/Cellar/tesseract/4.    1.1/bin/tesseract
    ""
