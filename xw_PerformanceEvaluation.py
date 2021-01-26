#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:34:27 2020

@author: LuZhongyan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from xw_IrisMatching import *


def get_CRR(train_vector, test_vector, train_y, test_y, lda_components):
    
    # matching
    acc_l1 = []
    acc_l2 = []
    acc_cosine = []
    
    for n in lda_components: 
        l1, l2, c = KNN_Matching(train_vector, test_vector, train_y, test_y, n)
        acc_l1.append(l1)
        acc_l2.append(l2)
        acc_cosine.append(c)
    
    # plot
    plt.figure()
    plt.plot(lda_components, acc_l1, linewidth=2)
    plt.plot(lda_components, acc_l2, linewidth=2)
    plt.plot(lda_components, acc_cosine, linewidth=2)
    plt.xlabel('Dimensionality of the feature vector')
    plt.ylabel('Correct Recognition Rate')
    plt.title('Recognition results using features of different dimensionality')
    plt.legend(['L1', 'L2', 'Cosine'])
    plt.show() 


def get_table3(train_vector, test_vector, train_y, test_y, n):

    print('Preparing for TABLE 3...')
    l1_origin, l2_origin, c_origin = KNN_Matching(train_vector, test_vector, train_y, test_y, None)
    l1_reduced, l2_reduced, c_reduced = KNN_Matching(train_vector, test_vector, train_y, test_y, n)
    
    table3 = pd.DataFrame({'Original Feature Set': [l1_origin, l2_origin, c_origin], 
                           'Reduced Feature Set': [l1_reduced, l2_reduced, c_reduced]
                           })
    table3.index = ['L1 distance measure', 'L2 distance measure','Cosine similarity measure']

    print(table3)

  
def get_ROC(match_cosine, cosine_min, test_y, threshold):

     
    TN, FN, FP, TP = 0,0,0,0
    false_match_rate = []  
    false_non_match_rate = []
    
    # compare the cosine distance with each threshold value
    for th in threshold:
        for i, d in enumerate(cosine_min):
            
            # if cosine distance < threshold value, then fail to reject H0
            if d <= th:
                if match_cosine[i] == test_y[i]: # match
                    TN += 1
                else:
                    FN += 1 
            else:
                if match_cosine[i] == test_y[i]: # match
                    FP += 1
                else:
                    TP += 1
                    
        # calculate the false_match_rate, false_non_match_rate
        if FP > 0 or TN > 0:
            false_match_rate.append( FN/(FN + TP) )
        if FN > 0 or TP > 0:
            false_non_match_rate.append( FP/(FP + TN) )

    print("preparing table for False Match and False Nonmatch Rates with Different Threshold Values...")
    table = pd.DataFrame({'Threadshold': threshold, 
                          'False Match Rate': false_match_rate, 
                          'False Non-Match Rate': false_non_match_rate})
    table = table.iloc[6:9,:].set_index('Threadshold')
    print(table)

    print("preparing the FMR-FNMR curve...")
    plt.plot(false_match_rate, false_non_match_rate)
    plt.xlabel("False Match Rate")
    plt.ylabel("False Non-Match Rate")
    plt.title("FMR and FNMR Curve")
    plt.show()
  
    


    