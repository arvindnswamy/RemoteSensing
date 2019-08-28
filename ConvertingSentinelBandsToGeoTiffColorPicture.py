#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 11:23:39 2019

@author: arvindn
"""

import cv2
import  os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import rasterio as rio

workingdir = '/home/arvindn/Research/TopicsOfInterest/Agriculture/Notes/SentinelImages/S2B_MSIL1C_20190807T050659_N0208_R019_T43QHV_20190807T085741.SAFE/GRANULE/L1C_T43QHV_A012629_20190807T051417/IMG_DATA'
os.chdir(workingdir)

filename = 'T43QHV_20190807T050659'

bandRED = '04'
bandGREEN = '03'
bandBLUE = '02'
imageR2rio = rio.open(filename+'_B' + bandRED + '.jp2')
imageG2rio = rio.open(filename+'_B' + bandGREEN + '.jp2')
imageB2rio = rio.open(filename+'_B' + bandBLUE + '.jp2')

imageR2 = imageR2rio.read(1).astype('uint16')
imageG2 = imageG2rio.read(1).astype('uint16')
imageB2 = imageB2rio.read(1).astype('uint16')

pX, pY = imageR2.shape



image2comp = np.zeros((pX, pY, 3), dtype=np.uint8)
image2comp[:,:,0] = cv2.equalizeHist(np.uint8(cv2.normalize(imageB2, None, 0, 255, cv2.NORM_MINMAX)))
image2comp[:,:,1] = cv2.equalizeHist(np.uint8(cv2.normalize(imageG2, None, 0, 255, cv2.NORM_MINMAX)))
image2comp[:,:,2] = cv2.equalizeHist(np.uint8(cv2.normalize(imageR2, None, 0, 255, cv2.NORM_MINMAX)))



filenameToBeWritten = filename +'_B02B03B04_equalized_uint8.tiff'

crsfile = imageR2rio
"""
with rio.open('./'+filenameToBeWritten,'w',driver='Gtiff',
                          width=pX, 
                          height = pY, 
                          count=3, crs=crsfile.crs, 
                          transform=crsfile.transform, 
                          dtype='uint8') as convertImage:
    convertImage.write(imageB2[:,:,0], 1)
    convertImage.write(imageG2[:,:,0], 2)
    convertImage.write(imageR2[:,:,0], 3)
    convertImage.close()
"""

with rio.open('./'+filenameToBeWritten,'w',driver='Gtiff',
                          width=pX, 
                          height = pY, 
                          count=3, crs=crsfile.crs, 
                          transform=crsfile.transform, 
                          dtype='uint8') as convertImage:
    for (k, arr) in [(1, image2comp[:,:,0]), (2, image2comp[:,:,1]), (3, image2comp[:,:,2])]:
        convertImage.write(arr, indexes=k)
    convertImage.close()
