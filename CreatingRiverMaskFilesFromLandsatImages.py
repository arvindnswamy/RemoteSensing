#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 17:43:37 2019

@author: arvindn
"""

#new addtion

import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob
import tarfile
from shutil import copyfile, move
import os

#band4cv2 = cv2.imread('LC08_L1TP_179077_20190606_20190606_01_RT_B5_Cropped.TIF', 0)
#edges = cv2.Canny(band4cv2, 100, 200)
#plt.imshow(edges)

os.chdir('/home/arvindn/Research/TopicsOfInterest/Agriculture/Notes/LandsatImages')

targzlist = glob.glob('LC08_L1TP_142049_*_T1.tar.gz')

for targzfile in targzlist:
    os.mkdir(targzfile.split('.')[0])
    move(targzfile, targzfile.split('.')[0])
    os.chdir(targzfile.split('.')[0])
    tar = tarfile.open(targzfile, "r:gz")
    tar.extractall()
    tar.close()
    os.chdir('..')
    
def untarLandsatScenes(sceneDirectory):
    os.chdir(sceneDirectory)
    targzlist = glob.glob('*.tar.gz')
    for targzfile in targzlist:
        os.mkdir(targzfile.split('.')[0])
        move(targzfile, targzfile.split('.')[0])
        os.chdir(targzfile.split('.')[0])
        tar = tarfile.open(targzfile, "r:gz")
        tar.extractall()
        tar.close()
        os.chdir('..')

dirlist = glob.glob('LC08_L1TP_142049_*_T1')

for direc in dirlist:
    os.chdir(direc)
    band5cv2 = cv2.imread(direc+'_B5_ManualAdjustmentInGIMP.TIF', 0)
    
    ret, thresh = cv2.threshold(band5cv2, 50, 255, cv2.THRESH_BINARY_INV)
    
   # cv2.imwrite(direc+'_B5_ManualAdjustmentInGIMP_Threshold.png', thresh, [cv2.IMWRITE_PNG_COMPRESSION, 2])
    cv2.imwrite(direc+'_B5_ManualAdjustmentInGIMP_Threshold.png', thresh)
    os.chdir('..')


def adjustHistogram(sceneList, sceneListDir, band):
    os.chdir(sceneListDir)
    for sceneDir in sceneList:
        os.chdir(sceneDir)
        imgname = sceneDir+'_'+band+'.TIF'
        bandcv2 = cv2.imread(imgname, 0)
        
        bandcv2equalHist = cv2.equalizeHist(bandcv2)
        
        cv2.imwrite(imgname.split('.')[0] + '_equalizedHist.TIF', bandcv2equalHist)
        os.chdir('..')

for direc in dirlist:
    os.chdir(direc)
    copyfile(direc+'_B5_ManualAdjustmentInGIMP_Threshold.png', '../'+direc+'_B5_ManualAdjustmentInGIMP_Threshold.png')
    os.chdir('..')
    

#if you want to reduce the image size 
imglist = glob.glob('*_B5_ManualAdjustmentInGIMP_Threshold.png')

for imgfile in imglist:
    img = cv2.imread(imgfile, 0)
    scale_percent = 20 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(imgfile.split('.')[0]+'.jpg', resized, [int(cv2.IMWRITE_JPEG_QUALITY), 10])
