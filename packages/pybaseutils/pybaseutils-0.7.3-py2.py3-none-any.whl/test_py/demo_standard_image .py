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


def standard_images(image_dir, out_dir):
    image_list = file_utils.get_images_list(image_dir)
    for image_file in image_list:
        image = cv2.imread(image_file)
        # 限制图像最大分辨率,不超过1920
        out_image = image_utils.resize_image_clip(image, clip_max=1920)
        print(image.shape, out_image.shape)
        out_file = file_utils.create_dir(out_dir, None, os.path.basename(image_file))
        cv2.imwrite(out_file, out_image)


if __name__ == "__main__":
    image_dir = "/home/dm/nasdata/dataset-dmai/handwriting/word-det/soft-v2/JPEGImages"
    out_dir = "/home/dm/nasdata/dataset-dmai/handwriting/word-det/soft-v2/image"
    standard_images(image_dir, out_dir)
