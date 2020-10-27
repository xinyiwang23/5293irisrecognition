# 5293irisrecognition

## Overview

Our project focus on the iris recognition from an image sequence.

## Result and Limitation

* The number in the "reduced feature set" column is the result using LDA method.
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/IMG_2113.JPG)
* Recognition results (CRR) using features of different dimensionality in LDA method.
1[image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/result.png)
* We also compare the result with PCA method by taking number of components in [400,550,600,650,1000], which perform better than LDA by the CRR range in 0.89 to 0.90. When choosing the n_components = 1000, we got the best CRR which is 0.904.
* Limitation: 
  * Since we only choose the certain dimention in [50,60,70,80,90,100,107] as the samples, we have limit resources to analyze the iris texture information. The result might be better if we increasing the size of sample data.
  * Also we can improve the result by tuning parameter for the PCA and LDA method. For example, choosing different number of components and using cross validation to find the best one.

## File Description

There are total 7 files below.

### 1.Iris Localization

#### 1.1 Function name: irisLocalization

      - Take parameter: color image.

      - First Step: Find the center
        We first project the image in the vertical and horizontal direction and get an estimated the center (xp,yp) of the pupil by searching the minimum value of two coordinates (lowest row and column sum). Then binarize a region using a threshhold of 64 to localize the pupil by recalculate the center. 

      - Second step: Find circles
        We use Hough transform for detecting the circles for pupil and iris and draw the boundary. Return innerCircle and outterCircle in turple format and both of them contain the x and y coordinate of center and corresponding radius.

#### 1.2 Funtion name: irisLocalizationDrawing

* This function takes the excatly same steps as irisLocalization(). Besides, it also draws the image with two boundaries. Designed for testing, debugging, and visualizing.
* Take parameter: image file name.

### 2.Iris Normalization

#### 2.1 Function name: getDistance

      - Take parameter: Two data points in the format (x1, y1, x2, y2)
      - Return: The distance between these two points. (will be using as parameter in the function getLongRadius() below.)
      - This funtion will be called in the function getxy() below.

#### 2.2 Function name: getInverseTan

      - Take parameter: Two data points in the format (x1, y1, x2, y2)
      - Return: The inverse of tangent between two points. (will be using as parameter in the function getLongRadius() below.)
      - This funtion will be called in the function getxy() below.

#### 2.3 Function name: getLongRadius

      - Take parameter: Distance, outterCircle and the result in getInverseTan() in the format (distance, radius, theta)       
      - Return: The radius of the iris, which is longer than the radius of pupil.
      - This funtion will be called in the function getxy() below for calculating the (xi(theta), yi(theta)), which is the coordinate of the outer boundary point in the direction theta in the original image Io.

#### 2.4 Function name: getxy

      - Take parameter: X, Y, innerCircle and outterCircle that we get from the function irisLocalization()
      - Return: (x,y)
      - In this function, we project the original iris in a Cartesian coordinate system into a doubly dimensionless pseudopolar coordinate by taking the X,Y of the normalized image and finding the corresponding x,y from the round image. This funtion will be called in the function getNormalization() below

#### 2.5 Function name: getNormalization

      - Take parameter: image,innerCircle,outterCircle
      - Return: new image 
      - For each pixel in normalized image, find the value for the corresponding pixels in the original image by calling the function getxy() and fill in the value.

#### 2.6 Function name: getRotation ?????(return出来的是什么

      - Take parameter: image, degree
      - Return: 
      - This function takes normalized image and rotate the rectangle image to specified degree. It will be called in the function5.2 processImageWithRotation() below.

### 3.Image Enhancement

#### 3.1 Function name: enhancement

      - Take parameter: image
      - Return: enhanced image by equalizing the histogram of the image.

#### 3.2 Function name: imageEnhancementByParts

      - Take parameter: image
      - Return: enhanced image using histogram equalization by 32x32 pixels region.

#### 3.3 Function name: allEnhancement ?????(和上一个function有什么区别？

      - Take parameter: image
      - Return:

### 4.Feature Extraction

* The frequency and orientation information can identify the local spatial patterns of different irises in the texture analysis. Since we normalize the image before, the orientation information among irises will not be the major differences of irises. So in this section, we focus on the frequency information to extract features using even-symmetric Gabor filters from the enhanced image part.

#### 4.1 Function name: roi

      - Take parameter: image
      - Return: Top 48 rows of the image which is the Region of Interest
      - This funtion will be called in the function getFilteredImage() below.
      - According to the Li Ma's paper, the upper portion of a normalized iris image provides the most useful texture information for recognition.

#### 4.2 Function name: m1
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/m1.png)      
      - Take parameter: x, y, sigmaY
      - Return: Modulating function of the defined filter, corresponding to the function 3 in Li Ma's paper (page 6). Here, the frequency of the sinusoidal function f in the paper, is 1/sigmaY.
      - This funtion will be called in the function g() below.
      - Again, the reason that we use the defined filter is that the horizontal direction in the normalized image contains more information than other directions.

#### 4.3 Function name: g
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/g.png)   
      - Take parameter: x, y, siamgeX, sigmaY
      - Return: Kernels function in paper.
      - This funtion will be called in the function getKernel() below. 
      - Note, siamgeX and sigmaY are the space constants of the Gaussian envelope along the x and y axis. According to the paper, siamgeX and sigmaY for the first channel are 3 and 1.5, and 4.5 and 1.5 for the second channel.

#### 4.4 Function name: getKernel

      - Take parameter: siamgeX, sigmaY
      - Return: Calculates the Gabor Filter with specified siamgeX,sigmaY
      - This funtion will be called in the function getFilteredImage() below.

#### 4.5 Function name: getFilteredImage

      - Take parameter: image, sigmaX, sigmaY
      - Return: calculates the convolve of image and filter

#### 4.6 Function name: getFeatureVector

      - Take parameter: Two filtered image (f1, f2).
      - Return: 1D feature vector with 1536 feature components (mean & sd for each blocks), since the the total number of small blocks is (48x512) / (8x8) x 2 = 768.
      - This function takes the two filtered Image and extracts mean and standard deviation corresponding to the function 5 in Li Ma's paper (page 7) for each 8x8 small block as the feature vector for a specific image.
       
### 5.Iris Matching

* We have the result from the last file that represent the iris image as a feature vector of length 1536. In this section, we first apply Fisher linear discriminant to reduce the dimension of the feature vector, then apply nearest center classifier.

#### 5.1 Function name: processImage

      - Take parameter: image file name
      - Return: feature vector of length 1536
      - In this function, we execute the procedure 1 to 4 that we wrote previousely, which are Localization, Normalization, Image Enhancement and Feature Extraction.
      - This funtion will be called in the function getDatabase() below.
      
#### 5.2 Function name: processImageWithRotation

      - Take parameter: image file name, rotation degree
      - Return: feature vector of length 1536
      - This is similar to processImage(), but since we want to define several templates which denotes the rotation angles for each training image, each training image has to be converted into several vector.
      - This funtion will be called in the function getDatabase() below.
      
#### 5.3 Function name: getDatabase

      - Take parameter: database folder (input as a number)
      - Return: loops through all the files in our database and transfer every image into a vector.
      - Note, Folder1 contains training image, so we do this with rotation and not doing rotation for Folder2.
      - This funtion will be called in the function7.1 runAll() below.
      
#### 5.4 Function name: getMatching

      - Take parameter: train data, test data, number of components for LDA, distanceMeasure is default to 3 (cosine distance)
      - Return: accuracy rate = correct matching / total
      - We do LDA for each vector and use l1,l2,and cosine distance by default to calculate the similarity between pictures. Note, distanceMeasure equal to 1 means to calculate the manhattan distance and else for euclidean distance. This function takes training and testing data and output the accuracy rate for our matching.
      - This funtion will be called in every function in the section Performance Evaluation below.

### 6.Performance Evaluation

All the functions in this section will be called in the next section Iris Recognition below.

#### 6.1 Function name: getCRRCurve

      - Take parameter: train data, test data
      - Return: plots the recognition results using features of different dimensionality of the LDA.
      
#### 6.2 Function name: getPCACurve

      - Take parameter: train data, test data
      - Return: plots the accuracy rate for different dimensions for PCA.
      - Within each PCA dimension, the maximum accuracy rate was calculated by trying LDA dimensions of 90,100,107 which approves to be the dimensions with highest accuracy rate in general.

#### 6.3 Function name: getTable

      - Take parameter: train data, test data
      - Return: prints the table of recognition results using different similarity measures
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/IMG_2113.JPG)

### 7.Iris Recognition

* This section run all the algorithm step by step including Localization, Normalization, Image Enhancement, Feature Extraction, Iris Matching, and Performance Envaluation.
* In addition to the LDA plot required by the project, we did PCA for dimension reduction and ploted accuracy curve for different PCA dimensions.

#### 7.1 Function name: runAll

* 
* After transfering the image into vector, get performance envaluation by calculating Acuracy curve for different PCA dimension reduction, CRR Curve, and recognition results tables.
      
#### 7.2 Function name: runAllReduced

Since the image analysis for all test and train images takes a very long time, we saved the result so the runAllReduced function does not run all the previous steps but directly load the data I saved before which saves a lot of time.

## Peer evaluation form

* Yujing Li (yl4268):
* Xuan Ren (xr2142):
* Xinyi Wang (xw2657):
