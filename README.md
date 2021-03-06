# 5293irisrecognition

## Overview

* Our project focus on the iris recognition from an image sequence. The data we use is CASIA Iris Image Database Version 1.0 (CASIA-IrisV1) which includes 756 iris images from 108 eyes. The whole project follows the steps in paper that written by L. Ma, T. Tan, Y. Wang and D. Zhang, “Personal Identification Based on Iris Texture Analysis”, IEEE Trans. on Pattern Analysis and Machine Intelligence (PAMI), Vol. 25, No. 12, pp.1519-1533, 2003.
* In our framework, there are total 6 steps to implement the iris recognition, which are Iris Localization, Iris Normalization, Image Enhancement, Feature Extraction, Iris Matching and Performance Envaluation. Each step will be explained in the "File Description" section.

## Result and Limitation

* The number in the "reduced feature set" column is the result using LDA method. Refer to the table3 in paper.
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/IMG_2113.JPG)
* Recognition results (CRR) using features of different dimensionality in LDA method. Refer to the Fig10 in paper.
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/result.png)
* We also compare the result with PCA method by taking number of components in [400,550,600,650,1000], which perform better than LDA by the CRR range in 0.89 to 0.90. When choosing the n_components = 1000, we got the best CRR which is 0.904.
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/result_pca.PNG)
* The Receiver Operating Characteristic (ROC) curve is False Match Rate (FMR) versus False NonMatch Rate (FNMR) curve, which measures the accuracy of matching process and shows the overall performance of an algorithm. Refer to the Fig13 in paper.
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/ROC.png)
* Refer to the table4 in paper.<br>
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/fmr_fnmr.png)

* Limitation: 
  * Since the dataset only contain 108 eyes, we have limit resources to analyze the iris texture information. The result might be better if we increasing the size of sample data.
  * Also we can improve the result by tuning parameter for the PCA and LDA method. For example, choosing different number of components and using cross validation to find the best one.
  * In the function6.1 getCRRCurve(), we only choose the certain dimention in [50,60,70,80,90,100,107] as the samples, which could also be changed into any integer between 1 and 107. By tuning the selected dimensions, we might also improve the result.
  
## File Description

There are total 7 files below.

### 1.Iris Localization

* First Step: Find the center<br>
  We first project the image in the vertical and horizontal direction and get an estimated the center (xp,yp) of the pupil by searching the minimum value of two coordinates (lowest row and column sum). Then binarize a region using a threshhold of 64 to localize the pupil by recalculate the center. 

* Second step: Find circles<br>
  We use Hough transform for detecting the circles for pupil and iris and draw the boundary.

#### 1.1 Function name: irisLocalization

      - Take parameter: color image.
      - Return: innerCircle and outerCircle in turple format and both of them contain the x and y coordinate of center and corresponding radius.

#### 1.2 Funtion name: irisLocalizationDrawing

      - This function takes the excatly same steps as irisLocalization(). Besides, it also draws the image with two boundaries. Designed for testing, debugging, and visualizing.
      - Take parameter: image file name.
      - Return: Same as above

### 2.Iris Normalization

* This section implement the functions of the normalizition part in paper.

#### 2.1 Function name: getDistance

      - Take parameter: Two data points in the format (x1, y1, x2, y2)
      - Return: The distance between these two points. (will be using as parameter in the function getLongRadius() below.)
      - This funtion will be called in the function getxy() below.

#### 2.2 Function name: getInverseTan

      - Take parameter: Two data points in the format (x1, y1, x2, y2)
      - Return: The inverse of tangent between two points. (will be using as parameter in the function getLongRadius() below.)
      - This funtion will be called in the function getxy() below.

#### 2.3 Function name: getLongRadius

      - Take parameter: Distance, outerCircle and the result in getInverseTan() in the format (distance, radius, theta)       
      - Return: The radius of the iris, which is longer than the radius of pupil.
      - This funtion will be called in the function getxy() below for calculating the (xi(theta), yi(theta)), which is the coordinate of the outer boundary point in the direction theta in the original image Io.

#### 2.4 Function name: getxy

      - Take parameter: X, Y, innerCircle and outerCircle that we get from the function irisLocalization()
      - Return: (x,y)
      - In this function, we project the original iris in a Cartesian coordinate system into a doubly dimensionless pseudopolar coordinate by taking the X,Y of the normalized image and finding the corresponding x,y from the round image. This funtion will be called in the function getNormalization() below

#### 2.5 Function name: getNormalization

      - Take parameter: image,innerCircle,outerCircle
      - Return: new image 
      - For each pixel in normalized image, find the value for the corresponding pixels in the original image by calling the function getxy() and fill in the value.


### 3.Image Enhancement

* From last section, since we normalized the image, so the new image may not have high contrast. Therefore, in this section, we enhance the image by dividing them to small blocks with size 16x16 and calculate the mean of them to estimate the background illumination. Then we apply histogram equalization to enhance the image.

#### 3.1 Function name: enhancement

      - Take parameter: image
      - Return: enhanced image by equalizing the histogram of the image.

#### 3.2 Function name: imageEnhancementByParts

      - Take parameter: image
      - Return: enhanced image using histogram equalization by 32x32 pixels region.

### 4.Feature Extraction

* The frequency and orientation information can identify the local spatial patterns of different irises in the texture analysis. Since we normalize the image before, the orientation information among irises will not be the major differences of irises. So in this section, we focus on the frequency information to extract features using even-symmetric Gabor filters from the enhanced image part.

#### 4.1 Function name: region_interested

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
      - Take parameter: x, y, siamgX, sigmaY
      - Return: Kernels function in paper.
      - This funtion will be called in the function getKernel() below. 
      - Note, siamgeX and sigmaY are the space constants of the Gaussian envelope along the x and y axis. According to the paper, siamgeX and sigmaY for the first channel are 3 and 1.5, and 4.5 and 1.5 for the second channel.

#### 4.4 Function name: getKernel

      - Take parameter: siamgX, sigmaY
      - Return: Calculates the Gabor Filter with specified siamgX,sigmaY
      - This funtion will be called in the function getFilteredImage() below.

#### 4.5 Function name: getFilteredImage

      - Take parameter: image, sigmaX, sigmaY
      - Return: calculates the convolution of image and filter

#### 4.6 Function name: getFeatureVector

      - Take parameter: Two filtered image (f1, f2).
      - Return: 1D feature vector with 1536 feature components (mean & sd for each blocks), since the the total number of small blocks is (48x512) / (8x8) x 2 = 768.
      - This function takes the two filtered Image and extracts mean and standard deviation corresponding to the function 5 in Li Ma's paper (page 7) for each 8x8 small block as the feature vector for a specific image.
       
### 5.Iris Matching

* We have the result from the last file that represent the iris image as a feature vector of length 1536. In this section, we first apply Fisher linear discriminant to reduce the dimension of the feature vector, then apply nearest center classifier.
      
#### Function name: getMatching

      - Take parameter: train data, test data, number of components for LDA, distanceMeasure is default to 1 (cosine distance)
      - Return: accuracy rate = correct matching / total, predicted result and cosine distance
      - We do LDA for each vector and use l1,l2,and cosine distance by default to calculate the similarity between pictures. Note, distanceMeasure equal to 2 means to calculate the manhattan distance and else for euclidean distance. This function takes training and testing data and output the accuracy rate for our matching.
      - This funtion will be called in every function in the section Performance Evaluation below.

### 6.Performance Evaluation

* All the functions in this section will be called in the next section Iris Recognition below. We evalute the perform of the model and transform the result into CRR curve and table as paper's table3 & Fig10. Also, we calculate the ROC curve which is False Match Rate (FMR) versus False NonMatch Rate (FNMR) curve and return the corresponding table.

#### 6.1 Function name: getCRRCurve

      - Take parameter: train data, test data
      - Return: plots the recognition results using features of different dimensionality of the LDA.
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/result.png) 

#### 6.2 Function name: getTable

      - Take parameter: train data, test data
      - Return: prints the table of recognition results using different similarity measures
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/IMG_2113.JPG)      

#### 6.3 Function name: getPCACurve

      - Take parameter: train data, test data
      - Return: plots the accuracy rate for different dimensions for PCA.
      - Within each PCA dimension, the maximum accuracy rate was calculated by trying LDA dimensions of 90,100,107 which approves to be the dimensions with highest accuracy rate in general.
      
#### 6.4 Function name: metrics_calculator

      - Take parameter: predicted result, cosine distance that obtained from function5 and the threashold that we need to using for calculate FMR, FNMR
      - Return: false match rate, false non match rate.
      - This funtion will be called in the function getROCCurve() below.   
      
#### 6.5 Function name: getROCCurve

      - Take parameter: train data, test data
      - Return: plots the ROC table and figure.
      - The threashold choosing here is from 0.1 to 0.7.
![image](https://github.com/xinyiwang23/5293irisrecognition/blob/main/image/ROC.png)

### 7.Iris Recognition

* This section run all the algorithm step by step including Localization, Normalization, Image Enhancement, Feature Extraction, Iris Matching, and Performance Envaluation.
* In addition to the LDA plot required by the project, we did PCA for dimension reduction and ploted accuracy curve for different PCA dimensions.

#### 7.1 Function name: processImage

      - Take parameter: image file name, rotation degree(if needed)
      - Return: feature vector of length 1536
      - In this function, we execute the procedure 1 to 4 that we wrote previousely, which are Localization, Normalization, Image Enhancement and Feature Extraction.
      - Since the paper need to obtain approximate rotation invariance, we unwrap the iris ring at different rotation angles to each traing image.
      - This funtion will be called in the function getDatabase() below.     
      
#### 7.2 Function name: getDatabase

      - Take parameter: database folder (input as a number)
      - Return: loops through all the files in our database and transfer every image into vectors.
      - Note, Folder1 contains training image, so we do this with rotation and not doing rotation for Folder2.
      - This funtion will be called in the function main() below.

#### 7.3 Function name: main

* First Step is data transformation. 
* After transfering the image into vector, get performance envaluation by calculating Acuracy curve for CRR Curve, recognition results tables, different PCA dimension reduction, ROC curve and table.
      
#### 7.4 Function name: reduce

* Since the image analysis for all test and train images takes a very long time, we saved the result so the reduce function does not run all the previous steps but directly load the data I saved before which saves a lot of time.

## Peer evaluation form

* Yujing Li (yl4268): Iris Localization, Iris Normalization, Image Enhancement
* Xuan Ren (xr2142): Feature Extraction, Iris Matching， Performance Evaluation
* Xinyi Wang (xw2657): Performance Evaluation, Iris Recognition, Readme file
