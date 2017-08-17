
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
#[Ref_filePath, Ref_dirPath] = mm.openFileDia("D:/Python/Data/", "*.png")
#imR = cv2.imread(Ref_filePath,-1)
#rot_imR = np.rot90(imR,3)

# global variables
numberOfIm = 15
numberOfRun = 30
imDim = np.array([512,640])
BadPixMap=np.zeros([imDim[0],imDim[1]],np.uint8)

imArray=np.zeros((imDim[0],imDim[1],numberOfIm),dtype=np.int16)
imVectorArray = np.zeros((imDim[0]*imDim[1],numberOfIm),dtype=np.double)

for j in range(0,numberOfRun):
    for i in range(0, numberOfIm):
        range(j*numberOfIm, j*numberOfIm+numberOfIm)
        filename = DirPath+'image_'+("%0.6i"% (j*numberOfIm+i))+'.tif.tif'
        print(filename)
        imArray[:,:,i] = cv2.imread(filename,-1)
        imVectorArray[:,i]  = cv2.imread(filename,-1).reshape(imDim[0]*imDim[1])
        cv2.imshow('image',imArray[:,:,i])
        cv2.waitKey(10)
        if i==numberOfIm-1:
            print('images are loaded: i='+str(i)+' last im name: '+filename)
            cv2.destroyAllWindows()
    print(j)   
    BadPixMap = BadPixMap + mm.bdPixel_searcher(imVectorArray, 4, 1, imDim, False, 1)
    #print(BadPixMap_tmp.shape)
    #BadPixMap = BadPixMap + 



    
    





























