#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 23:14:05 2020

@author: LuZhongyan
"""


import numpy as np
import cv2
import matplotlib.pyplot as plt


def IrisLocalization(img):
    
    # estimate center
    horizontal_center_index = np.mean(img,0).argmin()
    vertical_center_index = np.mean(img,1).argmin()
      
    # resize img to 120 * 120 by its estimated center
    img120 = img[np.arange(vertical_center_index - 60, 
                           min(279, vertical_center_index+60)),:][:, np.arange(horizontal_center_index-60, min(319,horizontal_center_index+60))]
    
    # mask for pupil
    ret, pupil_th = cv2.threshold(img120, 60, 255, cv2.THRESH_BINARY)
    

    # adjust estimated center using mask
    horizontal120 = np.mean(pupil_th,0).argmin() - 60
    vertical120 = np.mean(pupil_th,1).argmin() - 60
    
    horizontal_center_index += horizontal120
    vertical_center_index += vertical120       
    
    # adjust 120 * 120 image
    img120 = img[np.arange(vertical_center_index - 60, 
                           min(279, vertical_center_index+60)),:][:, np.arange(horizontal_center_index-60, min(319,horizontal_center_index+60))]
    
    # adjusted mask for finding circle
    ret, pupil_th = cv2.threshold(img120, 60, 255, cv2.THRESH_BINARY)

    # detect pupil circle
    for loop in range(1,5):
        pupil_circles = cv2.HoughCircles(pupil_th, cv2.HOUGH_GRADIENT, 5.1, 300,
                                         param1 = 50, param2 = 10,
                                         minRadius = (35 - loop),
                                         maxRadius = (50 + loop))
        if type(pupil_circles) != type(None):
            break
        else:
            pass
    
    pupil_circles = np.round(pupil_circles).astype("int").flatten()
    
    # convert the relative coordinates of pupil center, pupil radius, 
    # to absolute coordinates.
    inner = [horizontal_center_index - 60 + pupil_circles[0],
             vertical_center_index - 60 + pupil_circles[1],
             pupil_circles[2]]   
                    
    outer = [inner[0], inner[1], inner[2]+60]
        
    return inner, outer   


def draw(img):
    
    draw_img = img.copy()

    horizontal_center_index = np.mean(img,0).argmin()
    vertical_center_index = np.mean(img,1).argmin()
      
    # resize img to 120 * 120 by its estimated center
    img120 = img[np.arange(vertical_center_index - 60, 
                           min(279, vertical_center_index+60)),:][:, np.arange(horizontal_center_index-60, min(319,horizontal_center_index+60))]
    plt.imshow(img120, cmap = 'gray')
    plt.show()
    
    # mask for pupil
    ret, pupil_th = cv2.threshold(img120, 60, 255,cv2.THRESH_BINARY)
    plt.imshow(pupil_th)
    plt.show()
        
    horizontal120 = np.mean(pupil_th,0).argmin() - 60
    vertical120 = np.mean(pupil_th,1).argmin() - 60
    
    horizontal_center_index += horizontal120
    vertical_center_index += vertical120   
    
    # resize img to 120 * 120 by its estimated center
    img120 = img[np.arange(vertical_center_index - 60, 
                           min(279, vertical_center_index+60)),:][:, np.arange(horizontal_center_index-60, min(319,horizontal_center_index+60))]
    plt.imshow(img120, cmap = 'gray')
    plt.show()
    
    # mask for pupil
    ret, pupil_th = cv2.threshold(img120, 60, 255,cv2.THRESH_BINARY)
    plt.imshow(pupil_th)
    plt.show()
    
    for loop in range(1,5):
        pupil_circles = cv2.HoughCircles(pupil_th, cv2.HOUGH_GRADIENT, 5.1, 300,
                                         param1 = 30, param2 = 20,
                                         minRadius = (35 - loop),
                                         maxRadius = (50 + loop))
        if type(pupil_circles) != type(None):
            break
        else:
            pass
    
    pupil_circles = np.round(pupil_circles).astype("int").flatten()
    
    # convert the relative coordinates of pupil center, pupil radius, 
    # to absolute coordinates.
    inner = [horizontal_center_index - 60 + pupil_circles[0],
             vertical_center_index - 60 + pupil_circles[1],
             pupil_circles[2]]   
                    
    outer = [inner[0], inner[1], inner[2]+60]
                
    '''
        # resize img to 220 * 240 by the estimated center
        img240 = img[np.arange(inner[1]-110, min(279, inner[1] + 110)),
                     :][:, np.arange(inner[0]-120, min(319,inner[0]+120))]
        
        # mask for iris
        ret, iris_th = cv2.threshold(img240,140,255,cv2.THRESH_BINARY)

        # detect iris circle
        iris_circles = cv2.HoughCircles(iris_th, cv2.HOUGH_GRADIENT, 1, 250,
                                        param1 = 30, param2 = 10,
                                        minRadius = 98, maxRadius = 120)
        
        if iris_circles is not None:
            iris_circles = np.round(iris_circles).astype("int").flatten()
            outer = [inner[0] - 120 + iris_circles[0],
                     inner[1] - 110 + iris_circles[1],
                     iris_circles[2]]
        else:
            pass
    '''
                  
    # draw pupil
    draw1 = cv2.circle(draw_img, (inner[0], inner[1]), inner[2], 
                       color=(0, 255, 0), thickness=2)
    
    # draw iris
    draw1 = cv2.circle(draw_img, (outer[0], outer[1]), outer[2], 
                       color=(0, 255, 0), thickness=2)
    
    plt.imshow(draw1, cmap = 'gray')
    plt.show()
        
    return inner, outer
                           
