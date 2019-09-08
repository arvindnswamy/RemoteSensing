import os
import rasterio
from glob import glob
import matplotlib.pyplot as plt
import gdal
import cv2
import numpy as np
import scipy.misc as sm



# xmin, xmax, ymin, ymax = [], [], [], []


# the_save_directory = "/Users/praga/Documents/Analytics/Earth Analytics/Landsat Images/"
#
#
# for image_path in glob(os.path.join(the_save_directory, '*/*B10.TIF')):
#
#     with rasterio.open(image_path) as src_raster:
#         xmin.append(src_raster.bounds.left)
#         xmax.append(src_raster.bounds.right)
#         ymin.append(src_raster.bounds.bottom)
#         ymax.append(src_raster.bounds.top)
#


file_directory = "/Users/praga/Documents/Analytics/Earth Analytics/Landsat Images/"
scene_name = "LC08_L1TP_013032_20180131_20180207_01_T1"

dirname = file_directory + scene_name + "/"

# B4 bands are red: 0.64 - 0.67 micrometer
# B3 band is green: 0.53 - 0.59 micrometer
# B2 band is blue: 0.45 - 0.51 micrometer


MTLfilename = dirname + scene_name + '_MTL.txt'

d = {}

with open(MTLfilename) as f:
    for line in f:
        if '=' in line:
            (key, val) = line.split(" = ")
            key = key.strip()
            val = val.strip()
            d[key] = val

imageR2 = cv2.imread(dirname + scene_name + '_B4.TIF')
imageG2 = cv2.imread(dirname + scene_name + '_B3.TIF')
imageB2 = cv2.imread(dirname + scene_name + '_B2.TIF')

pX, pY, pZ = imageR2.shape

# the shape of the array is [7781 x 7651 x 3]


image2comp = np.zeros((pX, pY, pZ), dtype=np.uint8)  # Initialize a zero array with the size of imageR2

image2comp[:, :, 0] = imageR2[:, :, 0]
image2comp[:, :, 1] = imageG2[:, :, 0]
image2comp[:, :, 2] = imageB2[:, :, 0]


f, (ax1, ax2, ax3) = plt.subplots(3, figsize=(12,12), sharex=True)

col = ('b', 'g', 'r')
band = ('B2', 'B3', 'B4')


# Normalize the bands

for i, colors in enumerate(col):
    histr = cv2.calcHist([image2comp], [i], None, [256], [1,256])
    #ax1.plot(histr, color=colors)

imageR2equ = cv2.equalizeHist(imageR2[:, :, 0])  # Why?
imageG2equ = cv2.equalizeHist(imageG2[:, :, 0])
imageB2equ = cv2.equalizeHist(imageB2[:, :, 0])


image2equcomp = np.zeros((pX, pY, pZ), dtype=np.uint8)
image2equcomp[:, :, 0] = imageR2equ
image2equcomp[:, :, 1] = imageG2equ
image2equcomp[:, :, 2] = imageB2equ
#cv2.imwrite(dirname + '_B2B3B4_EqualHist.TIF', image2equcomp)


for i, colors in enumerate(col):
    histrE = cv2.calcHist([image2equcomp], [i], None, [256], [1, 256])
    ax2.plot(histrE, color=colors)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # What does this do?

imageR2clahe = clahe.apply(imageR2[:, :, 0])
imageG2clahe = clahe.apply(imageG2[:, :, 0])
imageB2clahe = clahe.apply(imageB2[:, :, 0])
image2CLAHEcomp = np.zeros((pX, pY, pZ), dtype=np.uint8)
image2CLAHEcomp[:, :, 0] = imageR2clahe
image2CLAHEcomp[:, :, 1] = imageG2clahe
image2CLAHEcomp[:, :, 2] = imageB2clahe
#cv2.imwrite(dirname + '_B2B3B4_CLAHEHist.TIF', image2CLAHEcomp)

for i, colors in enumerate(col):
    histrC = cv2.calcHist([image2CLAHEcomp], [i], None, [256], [1, 256])
    ax3.plot(histrC, color=colors)

ax3.set_xlim([1, 256])
f
f.savefig('myfigure.png')


# Plot the true-color image
rgb = np.dstack((imageR2clahe, imageG2clahe, imageB2clahe))
plt.imshow(rgb)





b2_file = glob(file_directory + '**B2.TIF')  # blue band
b3_file = glob(file_directory + '**B3.TIF')  # green band
b4_file = glob(file_directory + '**B4.TIF')  # red band



def norm(band):
    """
    Normalize the values within the band array.

    :param band:
    :return:
    """
    band_min, band_max = band.min(), band.max()

    return ((band - band_min)/(band_max - band_min))


for i in range(len(b2_file)):

    # Open each band using gdal
    b2_link = gdal.Open(b2_file[i])
    b3_link = gdal.Open(b3_file[i])
    b4_link = gdal.Open(b4_file[i])

    # call the norm function on each band as array converted to float
    b2 = norm(b2_link.ReadAsArray().astype(np.float))
    b3 = norm(b3_link.ReadAsArray().astype(np.float))
    b4 = norm(b4_link.ReadAsArray().astype(np.float))

    # Create RGB
    rgb = np.dstack((b4, b3, b2))
    del b2, b3, b4

    # Visualize RGB
    plt.imshow(rgb)

    # # Export RGB as TIFF file
    # # Important: Here is where you can set the custom stretch
    # # I use min as 2nd percentile and max as 98th percentile
    # sm.toimage(rgb, cmin=np.percentile(rgb, 2),
    #            cmax=np.percentile(rgb, 98)).save(b2_file[i].split('_01_')[0] + '_RGB.tif')

