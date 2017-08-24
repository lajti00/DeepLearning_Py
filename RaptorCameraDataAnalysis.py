# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 13:18:36 2017

@author: imre.lajtos
This code created for Raptor camera stability analysis
"""
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import cv2
import pandas as pd 
import time as time
from  tkinter import *
from tkinter import filedialog
from astropy.stats import sigma_clip
from astropy.io import fits
import mymodules_ as mm
import sys
from pathlib import Path

[filePath, DirPath] = mm.openFileDia("D:/Python/Data/", "*.fits")
if filePath=="":
    print("select a file")
    sys.exit()
    



# global variables
DataColNames = ['#','ImID','Exposure Time','DarkAve','DarkMed','DarkStd','DarkMin','DarkMax','Number of saturated pixels (>= 15490)','Number of zero pixels (<=10)','Sensor temperature[C]','PCB temperature[C]','MeasFlag']
ImID = []
Index = []
counter = 0
ExposureTime = []
DarkAve = []
DarkMed = []
DarkStd = []
DarkMin = []
DarkMax = []
SatPixels = []
ZeroPixels = []
SensorTemp = []
PCBTemp = []
MeasFlag = []

numberOfIm = 13417
numberOfRun = 1
imDim = np.array([512,640])
BadPixMap=np.zeros([imDim[0],imDim[1]],np.uint8)
imArray=np.zeros((imDim[0],imDim[1],numberOfIm),dtype=np.int16)
imVectorArray = np.zeros((imDim[0]*imDim[1],numberOfIm),dtype=np.double)
CameraLog = False;
Darkflag = True;
MeasIDs = [1,2,3,4]
indx = 0;
cc = 0;
#temperature data

column_names = ['1','2', '3', '4', '5', '6', '7']
CameraLOGPath = DirPath+'RaptorNinox640_Raptor.log'
df_camera = pd.read_csv(CameraLOGPath,sep=' ',skiprows=5,low_memory=False, names = column_names)

# Image aq data
CameraLOGPath = DirPath+'RaptorTXT.txt'
my_file = Path(CameraLOGPath)
if my_file.is_file():
    # file exists
    column_names2 = ['1','2', '3', '4', '5', '6', '7', '8', '9']
    df_aqData = pd.read_csv(CameraLOGPath,sep=';',skiprows=0,low_memory=False, names = column_names2)
    CameraLog = True;
    
        

#processing 
for j in range(0,numberOfRun):
    for i in range(0, numberOfIm):
        range(j*numberOfIm, j*numberOfIm+numberOfIm)
        filename = DirPath+'image'+("%0.5i"% (j*numberOfIm+i))+'.fits'
        print(filename)
        imArray[:,:,i] = fits.getdata(filename)
        imVectorArray[:,i]  = imArray[:,:,i].reshape(imDim[0]*imDim[1])
        # Data frame elements
        Index.append(counter)
        ImID.append(filename)
        if CameraLog:
            ExposureTime.append(df_aqData['2'][j*numberOfIm+i])
        else:
            ExposureTime.append("NaN")
        
        #MeasFlag[MeasFlag[-20:-1]==indx]
        
        if len(DarkAve)>0:
            previousMed = DarkMed[-1]
        else:
            previousMed = np.median(imVectorArray[:,i])
        
        DarkAve.append(imVectorArray[:,i].mean())
        DarkMed.append(np.median(imVectorArray[:,i]))
        DarkStd.append(imVectorArray[:,i].std())
        DarkMin.append(imVectorArray[:,i].min())
        DarkMax.append(imVectorArray[:,i].max())
        SatPixels.append(len(imVectorArray[imVectorArray[:,i]>=15490,i]))
        ZeroPixels.append(len(imVectorArray[imVectorArray[:,i]<=10,i]))
        SensorTemp.append(float(df_camera['5'][j*numberOfIm+i].split(':')[1].split('\t')[0]))
        PCBTemp.append(float(df_camera['7'][j*numberOfIm+i].split(':')[1].split('\t')[0]))
        print(cc)
        if (abs((previousMed/DarkMed[-1])-1)) > 0.05 and cc>90:
            #indx += 1;
            indx +=1
            cc=-1;
        MeasFlag.append(MeasIDs[indx%4])
        cc +=1;
#        cv2.imshow('image',imArray[:,:,i])
#        cv2.waitKey(10)
#        time.sleep(0.1)
#        if i==numberOfIm-1:
#            print('images are loaded: i='+str(i)+' last im name: '+filename)
#            cv2.destroyAllWindows()
        counter +=1 
    print(j)   

#del df_aqData
del df_camera



DataSet = list(zip(Index,ImID, ExposureTime, DarkAve, DarkMed, DarkStd, DarkMin, DarkMax, SatPixels, ZeroPixels, SensorTemp, PCBTemp, MeasFlag))
df = pd.DataFrame(data = DataSet, columns=DataColNames[0:13])

df['DarkAve'][df['MeasFlag']==1].plot(title='DarkAve')

df_sumary = df[['DarkAve','DarkMed','DarkStd','DarkMin','DarkMax','Number of saturated pixels (>= 15490)',
                'Number of zero pixels (<=10)','Sensor temperature[C]','PCB temperature[C]','Exposure Time']].groupby('Exposure Time').mean()
df_std = df[['DarkAve','DarkMed','DarkStd','DarkMin','DarkMax','Number of saturated pixels (>= 15490)',
                'Number of zero pixels (<=10)','Sensor temperature[C]','PCB temperature[C]','Exposure Time']].groupby('Exposure Time').std()



excelFile = DirPath+'output.xlsx'
writer = pd.ExcelWriter(excelFile)
df.to_excel(writer,'AllData')
df_sumary.to_excel(writer,'mean_forEachExposure')
df_std.to_excel(writer,'std_forEachExposure')

writer.save()
