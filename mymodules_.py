from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from astropy.stats import sigma_clip

def showImageCV(im):
    cv2.imshow('image',im)
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('messigray.png',im)
        cv2.destroyAllWindows()
		
def openFileDia(initialdir, fileType):
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = initialdir,title = "choose your file",filetypes = (("image files",fileType),("all files","*.*")))
    root.withdraw()
    filePath=root.filename
    dirPath = filePath[0:-1*len(filePath.split('/')[-1])]
    return [filePath, dirPath]
	
# filePath = mm.openFileDia()

def bdPixel_searcher(imVectorArray, sigma, iters, imDim, visualisation, imageVal):
    # imVectorArray [np array]: each lie coresponding an image dim1 = number of images dim2 = number of pixels in the image
    # sigma [int]: sigma parameter for classification and sigma clip
    # iters [int]: iteration of sigma clip
    # visualisation [Bool]
    # output image high value
    #imageVal = 255
    
    px_mean=imVectorArray.mean(axis=1)
    px_sd=imVectorArray.std(axis=1)
    print('Menan: '+str(px_mean.mean()))
    print('SD_mean: '+str(px_sd.mean()))
    if visualisation:
        plt.plot(px_mean)
        plt.ylabel('SD')
        plt.show()
    
    
    # Find the pixels with too high and too low sd
    
    MenanSDs = px_sd.mean()
    SDofSDs = px_sd.std()
    MenanOfMeans = px_mean.mean()
    SDofMeans = px_mean.std()

    absMinRange = np.array([0,MenanOfMeans-sigma*SDofMeans])
    absMaxRange = np.array([MenanOfMeans+sigma*SDofMeans,px_mean.max()])
    WrongGroup1 = np.where(px_sd<=MenanSDs-sigma*SDofSDs) #extrem low SD pixels 
    WrongGroup2 = np.where(px_sd>=MenanSDs+sigma*SDofSDs) #extrem high SD pixels 
    WrongGroup3 = np.where(px_mean<=absMinRange[1])
    WrongGroup4 = np.where(px_mean>=(2**16-500)) #extrem bright pixels
    WrongGroup5 = np.where(px_mean>=absMinRange[1])
    #Generating bad pixel image
    BadPixMap=np.zeros(imDim[0]*imDim[1],np.uint8)
    BadPixMap[WrongGroup1]=imageVal
    BadPixMap[WrongGroup2]=imageVal
    BadPixMap[WrongGroup3]=imageVal
    BadPixMap[WrongGroup4]=imageVal
    ##sigma clip methode
    ss = sigma_clip(px_mean, sigma=sigma, sigma_lower=None, sigma_upper=None, iters=iters)
#    good_only = ss.data[~ss.mask]
#    bad_only = ss.data[ss.mask]
    BadPixMap[ss.mask] = imageVal
    BadPixMap = BadPixMap.reshape(imDim[0],imDim[1])
    
    # visualisation antil any key interupt
    while visualisation:
        cv2.imshow('Bad pixel maps',BadPixMap)
        k = cv2.waitKey(50)       
        if k!=255:
            visualisation=False
            cv2.destroyAllWindows()
    return BadPixMap