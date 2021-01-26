#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 21:17:59 2020

@author: LuZhongyan
"""

import numpy as np
import scipy.signal

def m(x, y, f):
    return np.cos(2 * np.pi * f * np.sqrt(x ** 2 + y ** 2))

def gabor(x, y, dx, dy, f):
    return (1/(2 * np.pi * dx * dy)) * np.exp(-0.5 * (x ** 2 / dx ** 2 + y ** 2 / dy ** 2)) * m(x, y, f)

def get_kernel(dx, dy, f):
    
    kernel = np.zeros((9,9))

    for i in range(9):
        for j in range(9):
            kernel[i,j] = gabor((-4+j), (-4+i), dx, dy, f)    
    
    return kernel

def get_feature(enhanced_img):
    
    img = enhanced_img[:48, :]
    dx1, dx2 = 3, 4.5
    dy = 1.5
    f = 1 / dy
    
    kernel1 = get_kernel(dx1, dy, f)
    kernel2 = get_kernel(dx2, dy, f)
    
    convolution1 = scipy.signal.convolve2d(img, kernel1, mode='same')
    convolution2 = scipy.signal.convolve2d(img, kernel2, mode='same')
    
    vector = []
    i = 0
    while i < convolution1.shape[0]:
        j = 0
        while j < convolution1.shape[1]:
            
            block1 = convolution1[i:i+8, j:j+8]
            block2 = convolution2[i:i+8, j:j+8]
            
            mean_block1 = np.mean(np.abs(block1))
            vector.append(mean_block1)
            vector.append(np.mean(np.abs(np.abs(block1) - mean_block1)))
            
            mean_block2 = np.mean(np.abs(block2))
            vector.append(mean_block2)
            vector.append(np.mean(np.abs(np.abs(block2) - mean_block2)))
            
            j += 8
        i += 8
        
    return vector