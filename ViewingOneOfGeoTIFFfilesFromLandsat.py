#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 05:15:51 2019

@author: arvindn
"""

import cv2
import  os

os.chdir("/home/arvindn/Research/TopicsOfInterest/Agriculture/Notes/LandsatImages/LT05_L1TP_043020_19900528_20170131_01_T1")
image = cv2.imread("LT05_L1TP_043020_19900528_20170131_01_T1_B4.TIF")
cv2.namedWindow('B4', cv2.WINDOW_NORMAL)
cv2.resizeWindow('B4', 1000, 1000)
cv2.imshow('B4',  image)
image = cv2.imread("LT05_L1TP_043020_19900528_20170131_01_T1_B4.TIF")
cv2.imshow('B4',  image)
cv2.waitKey(0)
cv2.destroyAllWindows()