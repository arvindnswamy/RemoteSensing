# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import rasterio as rio
import numpy as np
import cv2

os.chdir('/home/arvindn/Research/TopicsOfInterest/Agriculture/Notes/SentinelImages/S2A_MSIL1C_20190709T184921_N0208_R113_T10SFG_20190709T222611.SAFE/GRANULE/L1C_T10SFG_A021131_20190709T185729/IMG_DATA')
band = '04'
filename = 'T10SFG_20190709T184921' + '_B' + band + '.jp2'
filenameToBeWritten = filename.split('.jp2')[0] + '_equalized_uint8.tiff'
imgtestband8A = rio.open(filename, 'r')

img1=np.uint8(cv2.normalize(imgtestband8A.read(1), None, 0, 255, cv2.NORM_MINMAX))

convertImage = rio.open('./'+filenameToBeWritten,'w',driver='Gtiff',
                          width=imgtestband8A.width, 
                          height = imgtestband8A.height, 
                          count=1, crs=imgtestband8A.crs, 
                          transform=imgtestband8A.transform, 
                          dtype='uint8')
convertImage.write(cv2.equalizeHist(img1),1)
convertImage.close()