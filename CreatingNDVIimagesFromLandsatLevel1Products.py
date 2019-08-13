#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:35:16 2019

@author: arvindn
"""

import rasterio as rio
import  os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
#landsatname = 'LC08_L1TP_192038_20190601_20190605_01_T1' #Sahara desert in Algeria
#landsatname = 'LC08_L1TP_192038_20190516_20190521_01_T1'#Sahara desert in Algeria

#landsatname = 'LC08_L1TP_179077_20190606_20190606_01_RT' #Kalahari desert and water
#landsatname = 'LC08_L1TP_179077_20190505_20190520_01_T1' #Kalahari desert and water

#landsatname = 'LC08_L1TP_204043_20190605_20190605_01_RT' #western sahara
#landsatname = 'LC08_L1TP_204044_20190605_20190605_01_RT' #western sahara
#landsatname = 'LC08_L1TP_203042_20190529_20190605_01_T1' #More western sahara
landsatname =  'LC08_L1TP_205042_20190527_20190605_01_T1' #More Western Sahara and water

landsatname = 'LC08_L1TP_144048_20180310_20180320_01_T1' #Hyderabad

os.chdir('/home/arvindn/Research/TopicsOfInterest/Agriculture/Notes/LandsatImages/BulkOrder1026953_Hyderabad/Landsat 8 OLI_TIRS C1 Level-1/'+landsatname)
landsatimage1 = landsatname + '_B4.TIF'
landsatimage2 = landsatname + '_B5.TIF'
rasterimB4 = rio.open(landsatimage1, 'r')
rasterimB5 = rio.open(landsatimage2, 'r')


band4 = rasterimB4.read(1).astype('float64')
band5 = rasterimB5.read(1).astype('float64')
NDVI = np.where(band4+band5==0., 0., (band5 - band4)/(band5 + band4)*1.0)

rasterNDVI_uint8 = np.abs(NDVI*255).astype('uint8')

ndviImage = rio.open('./ndviImage_uint8.tiff','w',driver='Gtiff',
                          width=rasterimB4.width, 
                          height = rasterimB4.height, 
                          count=1, crs=rasterimB4.crs, 
                          transform=rasterimB4.transform, 
                          dtype='uint8')
ndviImage.write(rasterNDVI_uint8,1)
ndviImage.close()

rasterNDVI_uint8 = (NDVI*255).astype('uint8')
ndviImage = rio.open('./ndviImage_uint8_NoAbs.tiff','w',driver='Gtiff',
                          width=rasterimB4.width, 
                          height = rasterimB4.height, 
                          count=1, crs=rasterimB4.crs, 
                          transform=rasterimB4.transform, 
                          dtype='uint8')
ndviImage.write(rasterNDVI_uint8,1)
ndviImage.close()

plt.imsave('testingNDVI.jpg', rasterNDVI_uint8)

ndviGeotiffImage = rio.open('ndviImage_uint8.tiff', 'r')

#rasterimB2 = rio.open('LC08_L1TP_014032_20170612_20170628_01_T1_B2.TIF', 'r')
#band2 = rasterimB2.read(1).astype('float64')
#
#rasterEVI = 2.5*((band5 - band4)/(band5 + 6*band4 - 7.5*band2 + 1))
#np.max(rasterEVI)
#rasterSAVI = 1.5*((band5 - band4)/(band5 + band4 + 0.5))

d = {}
           
MTLfilename = landsatname+'_MTL.txt'

with open(MTLfilename) as f:
    for line in f:
        if '=' in line:
            (key, val) = line.split(" = ")
            key = key.strip()
            val = val.strip()
            d[key] = val

landsatImageTIRS1 = landsatname + '_B10.TIF'

band_number1 = landsatImageTIRS1.split('_B')[1].split('.')[0]
band10 = rio.open(landsatImageTIRS1, 'r').read(1).astype('float64')

landsatImageTIRS2 = landsatname + '_B11.TIF'

band_number2 = landsatImageTIRS2.split('_B')[1].split('.')[0]
band11 = rio.open(landsatImageTIRS2, 'r').read(1).astype('float64')

Mlambda1 = float(d['RADIANCE_MULT_BAND_'+band_number1])
Alambda1 = float(d['RADIANCE_ADD_BAND_'+band_number1])

Mlambda2 = float(d['RADIANCE_MULT_BAND_'+band_number2])
Alambda2 = float(d['RADIANCE_ADD_BAND_'+band_number2])

Llambda1 = Mlambda1*band10+Alambda1
Llambda2 = Mlambda2*band11+Alambda2

K1_band1 = float(d['K1_CONSTANT_BAND_'+band_number1])
K2_band1 = float(d['K2_CONSTANT_BAND_'+band_number1])

K1_band2 = float(d['K1_CONSTANT_BAND_'+band_number2])
K2_band2 = float(d['K2_CONSTANT_BAND_'+band_number2])

Tlambda1 = K2_band1/np.log(K1_band1/Llambda1+1)
Tlambda2 = K2_band2/np.log(K1_band2/Llambda2+1) 

deltaT = Tlambda1-Tlambda2

plt.hist(deltaT.flatten(),bins=40,range=(-2,20))

print(np.abs(deltaT).mean(),np.abs(deltaT).std())

plt.imshow(Tlambda1, cmap='nipy_spectral'); plt.colorbar()

plt.imshow(Tlambda2, cmap='nipy_spectral'); plt.colorbar()