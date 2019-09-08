#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 05:15:51 2019

@author: arvindn
"""

import cv2
import  os
import pandas as pd
import shapefile
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.size'] = 24
matplotlib.rcParams['legend.fontsize'] = 24

#pathToLandsatFolder = input('Enter path to your Landsat folders')

pathToLandsatFolder = '/home/arvindn/Research/TopicsOfInterest/Agriculture/Notes/LandsatImages/'
dirname = input('Enter a Landsat folder name: ')

os.chdir(pathToLandsatFolder+dirname)

MTLfilename = dirname+'_MTL.txt'

#filename = open(MTLfilename, "r")

d = {}
"""
with open(MTLfilename) as f:
    for line in f:
        while True:
            try:
                (key, val) = line.split(" = ")
                key = key.strip()
                val = val.strip()
                d[key] = val
            except ValueError:
                print('Looks like you\'ve reached end of file')
                break
            
 """               

with open(MTLfilename) as f:
    for line in f:
        if '=' in line:
            (key, val) = line.split(" = ")
            key = key.strip()
            val = val.strip()
            d[key] = val

        
imageR2 = cv2.imread(dirname+'_B4.TIF')
imageG2 = cv2.imread(dirname+'_B3.TIF')
imageB2 = cv2.imread(dirname+'_B2.TIF')
pX, pY, pZ = imageR2.shape


image2comp = np.zeros((pX, pY, pZ), dtype=np.uint8)

image2comp[:, :, 0] = imageR2[:, :, 0]
image2comp[:, :, 1] = imageG2[:, :, 0]
image2comp[:, :, 2] = imageB2[:, :, 0]

cv2.imwrite(dirname+'_B2B3B4.TIF', image2comp)


f, (ax1, ax2, ax3) = plt.subplots(3, figsize=(12,12), sharex=True)
col = ('b','g','r')
band = ('B2', 'B3', 'B4')
for i, colors in enumerate(col):
    histr = cv2.calcHist([image2comp], [i], None, [256], [1,256])
    ax1.plot(histr, color=colors)


imageR2equ = cv2.equalizeHist(imageR2[:, :, 0])
imageG2equ = cv2.equalizeHist(imageG2[:, :, 0])
imageB2equ = cv2.equalizeHist(imageB2[:, :, 0])

image2equcomp = np.zeros((pX, pY, pZ), dtype=np.uint8)
image2equcomp[:, :, 0] = imageR2equ
image2equcomp[:, :, 1] = imageG2equ
image2equcomp[:, :, 2] = imageB2equ
cv2.imwrite(dirname+'_B2B3B4_EqualHist.TIF', image2equcomp)


for i, colors in enumerate(col):
    histrE = cv2.calcHist([image2equcomp], [i], None, [256], [1,256])
    ax2.plot(histrE, color=colors)
    
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
imageR2clahe = clahe.apply(imageR2[:,:,0])
imageG2clahe = clahe.apply(imageG2[:,:,0])
imageB2clahe = clahe.apply(imageB2[:,:,0])
image2CLAHEcomp = np.zeros((pX, pY, pZ), dtype=np.uint8)
image2CLAHEcomp[:,:,0] = imageR2clahe
image2CLAHEcomp[:,:,1] = imageG2clahe
image2CLAHEcomp[:,:,2] = imageB2clahe
cv2.imwrite(dirname+'_B2B3B4_CLAHEHist.TIF', image2CLAHEcomp)

for i, colors in enumerate(col):
    histrC = cv2.calcHist([image2CLAHEcomp], [i], None, [256], [1,256])
    ax3.plot(histrC, color=colors)
    
ax3.set_xlim([1,256])
f
