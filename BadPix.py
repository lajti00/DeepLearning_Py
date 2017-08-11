
# coding: utf-8

# In[1]:

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import cv2
from  tkinter import *
from tkinter import filedialog
from astropy.stats import sigma_clip
import mymodules_ as mm


# Open the images
[filePath, DirPath] = mm.openFileDia("D:/Python/Data/", "*.tif")
[Ref_filePath, Ref_dirPath] = mm.openFileDia("D:/Python/Data/", "*.png")
imR = cv2.imread(Ref_filePath,-1)
rot_imR = np.rot90(imR,3)

# global variables
numberOfIm = 15
imDim = np.array([512,640])


imArray=np.zeros((512,640,numberOfIm),dtype=np.int16)
imVectorArray = np.zeros((512*640,numberOfIm),dtype=np.double)
for i in range(0, numberOfIm+1):
    filename = filename = DirPath+'image_'+("%0.6o"% (i))+'.tif.tif'
    #print(filename)
    imArray[:,:,i-1] = cv2.imread(filename,-1)
    imVectorArray[:,i-1]  = cv2.imread(filename,-1).reshape(512*640)
    cv2.imshow('image',imArray[:,:,i-1])
    cv2.waitKey(10)
#     cv2.destroyAllWindows()
#     print(i)
    if i==numberOfIm:
        print('images are loaded: i='+str(i))
        cv2.destroyAllWindows()

BadPixMap = mm.bdPixel_searcher(imVectorArray, 3, 2, imDim, False, 255)




    
    





























