from __future__ import print_function
from PIL import Image, ImageTk
from matplotlib.pyplot import fill
from face_detector import detect
from tkinter import Tk, Label, Button
import threading
import datetime
import cv2
import os

class PhotoBoothApp:
    def __init__(self, vs, outputPath):
        # initialize the Video stream and file output Path
        # and also the last frame and thread that will take care of the video feed and display it in the GUI
        # and also the thread to stop the feed
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None


        # initialization of root window and the panel where the video feed will be displayed
        self.root = Tk()
        self.root.geometry("720x480")
        self.panel = None


        # Creation of snapshot button that will save the frame in your system
        btn = Button(self.root, text="Snapshot!", command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        #initialize the stop event thread and the video thread
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.root.title("PhotoBooth App")
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)


    def videoLoop(self):
        #While the window is not closed capture video.
        while not self.stopEvent.is_set():
            self.frame = self.vs.read() # read the frame captured.
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            face_detected = detect(self.frame) # add feature to detect faces.
            face_detected = cv2.cvtColor(face_detected, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(face_detected)
            image = ImageTk.PhotoImage(image) # show the image with face detected.

            # if no frame has been provided to the panel put the last frame inside it
            if self.panel is None:
                self.panel = Label(self.root, image=image)
                self.panel.image = image
                self.panel.pack(side="left", fill="both", expand="yes")
            # else just replace the frame with the most recent one
            else:
                self.panel.config(image=image)
                self.panel.image = image
    #Function to save the picture when pressing the button "Snapshot!"
    def takeSnapshot(self):
        # get the date and time of the snapshot
        ts = datetime.datetime.now()
        # generate a filename based on the timestamp
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        # create a path to save the file
        p = os.path.sep.join((self.outputPath, filename))
        # Sve the file 
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))
    
    # when closing the window destroy all processes.
    def onClose(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()