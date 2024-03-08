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

class VideoStream:
    #Class from grabbing frames from cv2 video capture.
    def __init__(self,src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame)=self.stream.read()
        self.stopped=False

    def start(self):
    # Creates a thread targeted at get(), which reads frames from CV2 VideoCapture.
        Thread = (target=self.get, args()).start()
        return self

    def get(self):
        #Continuously gets frames from CV2 VideoCapture and sets them as self.frame attribute
        while not self.stopped:
            (self.grabbed, self.frame)=self.stream.read()

    def get_video_dimensions(self):
        #get the dimensions of the video frame
        width=self.stream.get(cv2.CAR_PROP_FRAME_WIDTH)
        height=self.stream.get(cv2.CAR_PROP_FRAME_WIDTH)
        return int(width), int(height)
    def stop_process(self):
        self.stopped=True


class OCR:
    #Class for creating a pytesseract OCR process in a dedicated thread
    
    def __init__(self):
        self.boxes=None
        self.stopped=False
        self.exchanged=None
        self.language=None
        self.width=None
        self.crop_width=None
        self.height=None
        self.crop_height=None

    def start(self):
        #Creates a thread at OCR process
        Thread(target=self.ocr, args()).start()
        return self
    def set_exchange(self,video_stream):
        self.exchange=video_stream
        #Sets the self.exchange attribute with a reference to VideoStream class


    def set_language(self,language):
        self.language=language
        #Sets the self.language parameter

    def ocr(self):




