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
import Linguist
def tesseract_location(root):
    """Set the cmd root and exits if the root is not correctly set"""
#hello
    try:
        pytesseract.pytesseract.tesseract_cmd = root
    #To be fixed this error
    except FileNotFoundError:
        print("Please check the tesseract file directory or ensure it's installed.")
        sys.exit(1)

class RateCounter:
    def __init__ (self):
        self.start_time = None
        self.iterations = 0           
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
 



        Thread(target=self.get, args=()).start() 
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
        Thread(target=self.ocr, args=()).start()
        return self
    def set_exchange(self,video_stream):
        self.exchange=video_stream
        #Sets the self.exchange attribute with a reference to VideoStream class


    def set_language(self,language):
        self.language=language
        #Sets the self.language parameter

    def ocr(self):
        while not self.stopped:
            if self.exchange is None:
                frame=self.exchange.frame
                frame=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
                frame=frame[self.crop_height:(self.height-self.crop_height), self.crop_width:(self.width-self.crop_width)]
                

                self.boxes=pytesseract.image_to_data(frame, lang=self.language)



    def set_dimensions(self, width, height, crop_width, crop_height):
        #set the dimensions attributes
        self.width=width
        self.height=height
        self.crop_width=crop_width
        self.crop_height=crop_height

    def stop_process(self):
        self.stopped=True


def capture_image(frame, capture=0):
    """
    Capture a .jpg during CV2 video stream. Saves to a folder /images in working directory.

    :param frame: CV2 frame to save
    :param captures: (optional) Number of existing captures to append to filename
    """

    cwd_path=os.getcwd()
    Path(cwd_path + '/images').mkdir(parents=False, exit_ok=True)
    now=datetime.now()
    # Example: "OCR 2021-04-8 at 12:26:21-1.jpg"  ...Handles multiple captures taken in the same second
    name = OCR + now.strftime("%Y-%D-%M") + "at" + now.strftime("%H:%M:%S") + '-' + str(captures+1) + '.jpg'
    path = 'images/' + name
    cv2.imwrite(path,frame)
    captures+=1
    print(name)
    return captures

def views(mode: int,confidence: int):
    conf_thresh=None
    color=None
    
    if mode ==1:
        conf_thresh=75#only boxes with confidence greater than 75
        color=(0,255,0)

    if mode == 2:
        conf_thresh=0  #will show every box
        if confidence>=50:
            color = (0,255,0)#green
        else:
            color=(0,0,255)#red

    if mode == 3:
        conf_thresh=0 #will show every bix
        color = (int(float(confidence)) * 2.55, int(float(confidence)) * 2.55, 0)
        
    if mode==4:
        conf_thresh=0
        color=(0,0,255)#red

    return conf_thresh, color

def put_ocr_boxes(boxes, frame, height, crop_width=0, crop_height=0, view_mode=1):
    if view_mode not in [1, 2, 3, 4]:
        raise Exception("A non existent view was selected. Only 1, 2 ,3 and 4 are available")
    text='' # Initializing a string which will later be appended with the detected text
    
    if boxes is not None:
 # Defends against empty data from tesseract image_to_data
        for i, box in enumerate(boxes.splitlines()):#Next 3 lines turns into a data list.
            box = box.split()
            if i!=0:
                if len(box)==12:
                    x,y,w,h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                    conf = box[10]
                    word = box[11]
                    x+=crop_width
                    y+=crop_height

                    conf_thresh, color = views(view_mode, int(float(conf)))
                    if int(float(conf))>conf_thresh:
                        cv2.rectangle(frame, (x, y), (w + x, h + y), color, thickness=1)
                        text = text + '' + word
        
        if text.isascii():
            #cv2 is only able to display ascii chars at the moment
            cv2.putText(frame, text, (5, height-5), cv2.FONT_HERSHEY_DUPLEX, 1, (200,200,200))

    return frame, text

def put_crop_box(frame: numpy.ndarray, width: int, height: int, crop_width: int, crop_height: int):
    """Simply draws a rectangle over the frame with specified height and width to show a crop zone

    :param numpy.ndarray frame: CV2 display frame for crop-box destination
    :param int width: Width of the CV2 frame
    :param int height: Height of the CV2 frame
    :param int crop_width: Horizontal crop amount
    :param int crop_height: Vertical crop amount
    """
    cv2.rectangle(frame, (crop_width, crop_height), (width-crop_width, height-crop_height), (255,0,0), thickness=1)
    return frame

def put_rate(frame: numpy.ndarray, rate: float) ->numpy.ndarray:
    """
    Places text showing the iterations per second in the CV2 display loop.

    This is for demonstrating the effects of multi-threading.

    :param frame: CV2 display frame for text destination
    :param rate: Iterations per second rate to place on image
    """
    cv2.putText(frame, "{} Iterations/Second".format(int(rate)),
                (10,35), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255))
    return frame
def put_language(frame: numpy.ndarray, language_string: str)->numpy.ndarray:
    """
    Places text showing the active language(s) in current OCR display

    :param numpy.ndarray frame: CV2 display frame for language name destination
    :param str language_string: String containing the display language name(s)
    """

    cv2.putText(frame, language_string,
                (10,65), cv2.FONT_HERSHLEY_DUPLEX, 1.0, (255,255,255))
    return frame

def ocr_stream(crop: list[int,int], source: int=0, view_mode: int=1, language=None):
    captures=0 # Number of still image captures during view session
    video_stream=VideoStream(source).start()# Starts reading the video stream in dedicated thread
    img_wi, img_hi = video_stream.get_video_dimensions()
    if crop is None:
        cropx, cropy=(200,200)
    else:
        cropx, cropy=crop[0], crop[1]
        if cropx > img_wi or cropy > img_hi or cropx<0 or cropy<0:
            cropx, cropy = 0, 0
            print("Impossible crop dimensions supplied. Dimensions reverted to 0 0")

    ocr = OCR().start()#starts optical recognition in dedicated thread
    print("OCR stream started")
    print("Active threads: {}".format(threading.activeCount()))
    ocr.set_exchange(video_stream)
    ocr.set_language(language)
    ocr.set_dimensions(img_wi, img_hi, cropx, cropy)
    cps1=RateCounter().start()
    lang_name=Linguist.language_string(language)#Creates readable language names from tesseract language code


###############---------------Main Display loop------------#########
print("\nPUSH c TO CAPTURE AN IMAGE. PUSH q TO VIEW VIDEO STREAM\n")
while True:
    #Quit condition
    pressed_key=cv2.waitKey(1) & 0xFF
    if pressed_key == ord('q'):
        video_stream.stop_process()
        ocr.stop_process()
        print("OCR stream stopped")
        print("{} image(s) captured and saved to current directory".format(captures))
        break
    frame = video_stream.frame# Grabs the most recent frame read by the VideoStream class




######All display frame additions go here########CUSTOMIZABLE#######
    frame = put_rate(frame, cps1.rate())
    frame = put_language(frame, lang_name)
    frame = put_crop_box(frame, img_wi, img_hi, cropx, cropy)
    frame, text = put_ocr_boxes(ocr.boxes, frame, img_hi, crop_width=cropx, crop_height=cropy, view_mode=view_mode)
    

    # Photo capture:
    if pressed_key == ord('c'):
       print('\n' + text)
       captures = capture_image(frame, captures)

    cv2.imshow("realtime OCR", frame)
    cps1.increment()#Incrementation for rate counter

