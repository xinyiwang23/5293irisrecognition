#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 15:07:53 2020

@author: LuZhongyan
"""

import glob
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import scipy.signal
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial import distance


from xw_IrisLocalization  import *
from yl_IrisNormalization import *
from yl_ImageEnhancement import *
from xw_FeatureExtraction import *
from xw_IrisMatching import *
from xw_PerformanceEvaluation import *


# load train
imgs_train = [cv2.imread(file) for file in sorted(glob.glob('CASIA Iris Image Database (version 1.0)/*/1/*.bmp'))]
color_imgs_train = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in imgs_train]

i_train = 0
train_vector = []
train_y = np.repeat(np.arange(1,109), 3).tolist()
error_train = []

for img in color_imgs_train:
    try: 
        inner, outer = IrisLocalization(img)
        img_normal = IrisNormalization(inner, outer, img)
        img_enhance = ImageEnhancement(img_normal)
        train_vector.append(get_feature(img_enhance))

    except:
        error_train.append(i_train)
    i_train += 1
    continue

train_y = [y for e, y in enumerate(train_y) if e not in error_train]
print('Finish training image process') 


# load test
imgs_test = [cv2.imread(file) for file in sorted(glob.glob('CASIA Iris Image Database (version 1.0)/*/2/*.bmp'))]
color_imgs_test = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in imgs_test] 

i_test = 0
test_vector = []
test_y = np.repeat(np.arange(1,109), 4).tolist()
error_test = []

for img in color_imgs_test:
    try: 
        inner, outer = IrisLocalization(img)
        img_normal = IrisNormalization(inner, outer, img)
        img_enhance = ImageEnhancement(img_normal)
        test_vector.append(get_feature(img_enhance))
    except:
        error_test.append(i_test)
    i_test += 1
    continue

test_y = [y for e, y in enumerate(test_y) if e not in error_test]  
print('Finish testing image process') 


# matching and get CRR curves
print("preparing CRR curve...")
lda_components = [30,40,50,60,70,80,90,100]
get_CRR(train_vector, test_vector, train_y, test_y, lda_components)

# Here we use the result of LDA n_components = 50 to construct TABLE 3,
# TABLE4 and ROC curve

# table3
get_table3(train_vector, test_vector, train_y, test_y, 100)

# table4 and ROC
threshold = [i for i in np.arange(0.1, 0.7, 0.05)]
match_cosine, cosine_min = get_distance(train_vector, test_vector, train_y, test_y, 100)
get_ROC(match_cosine, cosine_min, test_y, threshold)


