# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import rasterio as rio
import numpy as np
import cv2
import matplotlib.pyplot as plt

workingdir = '/home/arvindn/Research/TopicsOfInterest/Agriculture/Notes/SentinelImages/S2B_MSIL1C_20190807T050659_N0208_R019_T43QHV_20190807T085741.SAFE/GRANULE/L1C_T43QHV_A012629_20190807T051417/IMG_DATA'
os.chdir(workingdir)
bandRED = '04'
bandNIR = '08'
filenameBase = 'T43QHV_20190807T050659'
filenameRED = filenameBase + '_B' + bandRED + '.jp2'
filenameNIR = filenameBase + '_B' + bandNIR + '.jp2'

imageRED = rio.open(filenameRED, 'r')
imageNIR = rio.open(filenameNIR, 'r')

bandRED = imageRED.read(1).astype('float64')
bandNIR = imageNIR.read(1).astype('float64')

NDVI = np.where(bandRED+bandNIR==0., 1., (bandNIR - bandRED)/(bandNIR + bandRED)*1.0)
pX, pY = NDVI.shape
NDVIcolorImage = np.zeros((pX, pY, 3))

ndviLims = np.array([-0.2, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0 ])
ndviColors = np.array([[0, 0, 0],
    [165./255,0,38./255],        
    [215/255,48/255,39/255],  
    [244/255,109/255,67/255],  
    [253/255,174/255,97/255],  
    [254/255,224/255,139/255], 
    [255/255,255/255,191/255], 
    [217/255,239/255,139/255], 
    [166/255,217/255,106/255], 
    [102/255,189/255,99/255],  
    [26/255,152/255,80/255],   
    [0,104/255,55/255]])

for k in np.arange(3):
    NDVIcolorImage[:,:,k] = np.where(NDVI <= -0.2, ndviColors[0,k]*255, NDVI)
    
for l in np.arange(1,len(ndviLims)):
    ndviLowerLim = ndviLims[l-1]
    ndviUpperLim = ndviLims[l]
    for k in np.arange(3):
        NDVIcolorImage[:,:,k] = np.where((NDVI > ndviLowerLim) & (NDVI <= ndviUpperLim), ndviColors[l,k]*255, NDVIcolorImage[:,:,k])
        
plt.imshow(NDVIcolorImage[:4000,00:4000,:]/255.0) #to show a portion of the image






filenameToBeWritten = filenameBase + '_NDVIcolor.tiff'

convertImage = rio.open('./'+filenameToBeWritten,'w',driver='Gtiff',
                          width=imageRED.width, 
                          height = imageRED.height, 
                          count=3, crs=imageRED.crs, 
                          transform=imageRED.transform, 
                          dtype='uint8')
convertImage.write(NDVIcolorImage[:,:,0].astype(np.uint8),indexes=1)
convertImage.write(NDVIcolorImage[:,:,1].astype(np.uint8),indexes=2)
convertImage.write(NDVIcolorImage[:,:,2].astype(np.uint8),indexes=3)
convertImage.close()

