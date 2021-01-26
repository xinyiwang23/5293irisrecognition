#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 14:49:38 2020

@author: LuZhongyan
"""

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial import distance


def get_lda(train_vector, test_vector, train_y, test_y, n):

    lda = LDA(n_components = n)
    lda.fit(train_vector, train_y)
    
    new_train_x = lda.transform(train_vector)
    new_test_x = lda.transform(test_vector)
    
    return new_train_x, new_test_x


def KNN_Matching(train_vector, test_vector, train_y, test_y, n = None):
    
    # whether fit LDA    
    if n:
        train_x, test_x = get_lda(train_vector, test_vector, train_y, test_y, n)
    else:
        train_x, test_x = train_vector, test_vector
        
    # L1
    knn_manhattan = KNeighborsClassifier(n_neighbors = 1, metric='manhattan')
    knn_manhattan.fit(train_x, train_y)
    acc_manhattan = knn_manhattan.score(test_x, test_y)

    # L2
    knn_euclidean = KNeighborsClassifier(n_neighbors = 1, metric='euclidean')
    knn_euclidean.fit(train_x, train_y)
    acc_euclidean = knn_euclidean.score(test_x, test_y)
    
    # Cosine distance
    knn_cosine = KNeighborsClassifier(n_neighbors = 1, metric='cosine')
    knn_cosine.fit(train_x, train_y)
    acc_cosine = knn_cosine.score(test_x, test_y) 
    
    return acc_manhattan, acc_euclidean, acc_cosine


def get_distance(train_vector, test_vector, train_y, test_y, n = None):

    # whether fit LDA
    if n:
        train_x, test_x = get_lda(train_vector, test_vector, train_y, test_y, n)   
    else:
        train_x, test_x = train_vector, test_vector
        
    # calculate distance
    # L1_min_index = []
    # L2_min_index = []
    cosine_min_index = []
    cosine_min = []
      
    for test_i in test_x:
        
        # Calculate the cosine distance between this test_i and every
        # feature vector in train
        
        #d_manhattan = []
        #d_euclidean = []
        d_cosine = []
        for train_i in train_x:
            # d_manhattan.append( distance.cityblock(test_i, train_i)) # L1
            # d_euclidean.append( distance.euclidean(test_i, train_i)) # L2
            d_cosine.append( distance.cosine(test_i, train_i)) # cosine
        
        
        #L1_min_index.append( d_manhattan.index(min(d_manhattan)))
        #L2_min_index.append( d_euclidean.index(min(d_euclidean)))
        
        # save the index of minimum distance
        cosine_min_index.append( d_cosine.index(min(d_cosine)))
        # also save the min cosine distance
        cosine_min.append( min(d_cosine))
   
    #match_L1 = [train_y[i] for i in L1_min_index]
    #match_L2 = [train_y[i] for i in L2_min_index]
    match_cosine = [train_y[i] for i in cosine_min_index]
     
    return match_cosine, cosine_min
    

