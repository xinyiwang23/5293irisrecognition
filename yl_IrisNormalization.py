#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 20:36:39 2020

@author: candy
"""

import numpy as np
import cv2

def IrisNormalization(inner, outer, img):
    
    pupil_radius = int(inner[2])
    
    iris_radius = 60

    # define equally spaced interval to iterate over
    n_samples = 360
    samples = np.linspace(0, 2 * np.pi, n_samples)[:-1]
    img_polar = np.zeros((iris_radius, n_samples))
    
    for r in range(iris_radius):
        for theta in samples:
            
            # get x and y for values on inner boundary
            x = int((r+ pupil_radius) * np.cos(theta) + inner[0])
            y = int((r+ pupil_radius) * np.sin(theta) + inner[1])

            try:
                # convert the original coordinates
                img_polar[r][int((theta * n_samples) / (2 * np.pi))] = img[y][x]
            
            except IndexError: 
                pass # ignores the out of bounds values
            continue
        
    img_normalize = cv2.resize(img_polar,(512,64))

    return img_normalize

