#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: pmeyyappan
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import shutil


all_scenes = pd.read_csv('http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', compression='gzip')


def download_landsat(specified_path, specified_row, save_directory):
    """
    Use this to download Landsat 8 images for a path, row combo.

    Finds all the scenes for the (path, row) and saves the scenes into individual folders.

    Filters are set to exclude the following scenes:
        1. Cloud Cover > 5%
        2. T2 scenes
        3. RT scenes

    :param specified_path:
    :param specified_row:
    :param save_directory: The folder within which the scenes need to be saved.

    :return:
    """

    path = specified_path
    row = specified_row
    base_directory = save_directory

    geography_filter = (all_scenes.path == path) & (all_scenes.row == row)

    cloud_cover_filter = (all_scenes.cloudCover <= 5)
    relevancy_filter = (~all_scenes.productId.str.contains('_T2')) & (~all_scenes.productId.str.contains('_RT'))

    relevant_scenes = all_scenes.loc[(geography_filter & cloud_cover_filter & relevancy_filter), :]

    for index, row in relevant_scenes.iterrows():

        # Print some the product ID
        print('\n', 'EntityId:', row.productId, '\n')
        print(' Checking content: ', '\n')

        # Request the html text of the download_url from the amazon server.

        response = requests.get(row.download_url)

        # If the response status code is fine (200)
        if response.status_code == 200:

            # Import the html to beautiful soup
            html = BeautifulSoup(response.content, 'html.parser')

            # Create the dir where we will put this image files.

            entity_dir = os.path.join(base_directory, row.productId)
            os.makedirs(entity_dir, exist_ok=True)

            # Second loop: for each band of this image that we find using the html <li> tag
            for li in html.find_all('li'):
                # Get the href tag
                file = li.find_next('a').get('href')

                print('  Downloading: {}'.format(file))

                # Download the files; code from: https://stackoverflow.com/a/18043472/5361345

                response = requests.get(row.download_url.replace('index.html', file), stream=True)

                with open(os.path.join(entity_dir, file), 'wb') as output:
                    shutil.copyfileobj(response.raw, output)

                del response

        else:
            print("Uh-Oh... something happened; Response Code - %s" % response.status_code)

    return


iter_path = 13
iter_row = 32

the_save_directory = "/Users/praga/Documents/Analytics/Earth Analytics/Landsat Images/"

download_landsat(specified_path=13, specified_row=32, save_directory=the_save_directory)


# all_scenes = s3_scenes[(s3_scenes.path == path) & (s3_scenes.row == row) & (s3_scenes.cloudCover <= 5) &
#                    (~s3_scenes.productId.str.contains('_T2')) & (~s3_scenes.productId.str.contains('_RT'))]

#print(all_scenes)  # Filtered for the (path, row) specified

#base_directory = "Landsat Images/"

# for i, row in scenes.iterrows():
#     # Print some the product ID
#     print('\n', 'EntityId:', row.productId, '\n')
#     print(' Checking content: ', '\n')
#
#     # Request the html text of the download_url from the amazon server.
#     # download_url example: https://landsat-pds.s3.amazonaws.com/c1/L8/139/045/LC08_L1TP_139045_20170304_20170316_01_T1/index.html
#
#     response = requests.get(row.download_url)
#
#     # If the response status code is fine (200)
#     if response.status_code == 200:
#
#         # Import the html to beautiful soup
#         html = BeautifulSoup(response.content, 'html.parser')
#
#         # Create the dir where we will put this image files.
#
#         entity_dir = os.path.join(base_directory, row.productId)
#         os.makedirs(entity_dir, exist_ok=True)
#
#         # Second loop: for each band of this image that we find using the html <li> tag
#         for li in html.find_all('li'):
#
#             # Get the href tag
#             file = li.find_next('a').get('href')
#
#             print('  Downloading: {}'.format(file))
#
#             # Download the files
#             # code from: https://stackoverflow.com/a/18043472/5361345
#
#             response = requests.get(row.download_url.replace('index.html', file), stream=True)
#
#             with open(os.path.join(entity_dir, file), 'wb') as output:
#                 shutil.copyfileobj(response.raw, output)
#
#             del response
#
#     else:
#         print("Uh-Oh... something happened; Response Code - %s" % response.status_code)