import os
from pathlib import Path
import sys
from datetime import datetime
import time
import threading 
from threading import Thread
import cv2
import numpy
import pytesseract  

def tesseract_location(root):
    """Set the cmd root and exits if the root is not correctly set"""

    try:
        pytesseract.pytesseract.tesseract_cmd = root
    except FileNotFoundError:
        print("Please check the tesseract file directory or ensure it's installed.")
        sys.exit(1)

class RateCounter:
     """
    Class for finding the iterations/second of a process
    
    `Attributes`
        start_time: indicates when the time.perf_counter() began
        iterations: determines number of iterations in the process

    `Methods:`
        start(): Starts a time.perf_counter() and sets it in the self.start_time attribute
        increment(): Increases the self.iterations attribute
        rate(): Returns the iterations/seconds
    """

    def __init__(self):
        self.start_time = None
        self.iteration = 0;
            
    def start(self):
        """Starts a time.perf_counter() and sets it in the self.start_time attribute"""
        self.start_time = time.perf_counter()
        return self

    def increment(self):
        """Increments self.iterations attribute"""
        sel.iteration += 1

    def rate(self):
        """Returns the iterations per seconds"""
        elapsed_time = (time.perf_counter() - self.start_time)

        return self.iterations/elapsed_time




