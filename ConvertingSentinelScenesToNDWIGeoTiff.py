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

os.chdir('/home/arvindn/Research/TopicsOfInterest/Agriculture/Notes/SentinelImages/S2A_MSIL1C_20190613T050701_N0207_R019_T44QLD_20190613T084200.SAFE/GRANULE/L1C_T44QLD_A020751_20190613T052314/IMG_DATA')
bandRED = '03'
bandNIR = '08'
filenameBase = 'T44QLD_20190613T050701'
filenameRED = filenameBase + '_B' + bandRED + '.jp2'
filenameNIR = filenameBase + '_B' + bandNIR + '.jp2'

imageRED = rio.open(filenameRED, 'r')
imageNIR = rio.open(filenameNIR, 'r')

bandRED = imageRED.read(1).astype('float64')
bandNIR = imageNIR.read(1).astype('float64')

NDWI = np.where(bandRED+bandNIR==0., 1., (bandRED - bandNIR)/(bandRED + bandNIR)*1.0)
pX, pY = NDWI.shape
NDWIcolorImage = np.zeros((pX, pY, 3))

ndwiColors = np.array([[0, 0.5, 0], [0,0,0.8]])

for k in np.arange(3):
    NDWIcolorImage[:,:,k] = np.where(NDWI <= 0.0, (ndwiColors[0,k]*(-NDWI)+1+NDWI)*255, (ndwiColors[1,k]*NDWI+1-NDWI)*255)
        
plt.imshow(NDWIcolorImage[:4000,00:4000,:]/255.0) #to show a portion of the image






filenameToBeWritten = filenameBase + '_NDWIcolor.tiff'

convertImage = rio.open('./'+filenameToBeWritten,'w',driver='Gtiff',
                          width=imageRED.width, 
                          height = imageRED.height, 
                          count=3, crs=imageRED.crs, 
                          transform=imageRED.transform, 
                          dtype='uint8')
convertImage.write(NDWIcolorImage[:,:,0].astype(np.uint8),indexes=1)
convertImage.write(NDWIcolorImage[:,:,1].astype(np.uint8),indexes=2)
convertImage.write(NDWIcolorImage[:,:,2].astype(np.uint8),indexes=3)
convertImage.close()

