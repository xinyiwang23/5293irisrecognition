#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 18:14:03 2020

@author: candy
"""

import numpy as np
import cv2

def ImageEnhancement(img):
    
    # enhance the image by means of histogram equalization in each 32x32 region
    
    #nrow = int(img.shape[0])
    #ncol = int(img.shape[1])
    
    #for row in range(0, nrow, 32):
    #    for col in range(0, ncol, 32):
    #        img_enhance = img[row:row+32, col:col+32]
    #        img_enhance = cv2.equalizeHist(np.array(img_enhance,dtype=np.uint8))
    #        img[row:row+32, col:col+32] = img_enhance
    
    image = np.array(img, dtype=np.uint8)
    image = cv2.equalizeHist(image)
    
    return image
