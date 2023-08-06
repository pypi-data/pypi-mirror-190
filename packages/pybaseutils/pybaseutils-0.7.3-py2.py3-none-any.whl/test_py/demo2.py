# -*-coding: utf-8 -*-
"""
    @Author : PKing
    @E-mail : 390737991@qq.com
    @Date   : 2022-12-31 11:37:30
    @Brief  :
"""
import os
import cv2
import time
from tqdm import tqdm
from multiprocessing import Pool
import numpy as np
from pybaseutils import file_utils, image_utils, base64_utils, time_utils, font_utils

if __name__ == "__main__":
    image_dir = "/home/dm/nasdata/dataset-dmai/handwriting/grid-det/grid_cross_points_images/grid_cross_points_soft_v1/images"
    image_list = file_utils.get_images_list(image_dir)
    for file in tqdm(image_list):
        image = cv2.imread(file)
        cv2.imwrite(file, image)
