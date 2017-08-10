from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import cv2
from  tkinter import *
from tkinter import filedialog
import mymodules_ as mm

# def showImageCV(im):
    # cv2.imshow('image',im)
    # k = cv2.waitKey(0)
    # if k == 27:         # wait for ESC key to exit
        # cv2.destroyAllWindows()
    # elif k == ord('s'): # wait for 's' key to save and exit
        # cv2.imwrite('messigray.png',im)
        # cv2.destroyAllWindows()
		
def openFileDia():
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "C:/",title = "choose your file",filetypes = (("image files","*.tif"),("all files","*.*")))
    #print (root.filename)
    root.withdraw()
    return root.filename
	
# filePath = mm.openFileDia()