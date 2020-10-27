# 5293irisrecognition

## Table of Contents


## Overview
Our project focus on the iris recognition from an image sequence.

## File Description

### Iris Localization

#### 1.Function name: irisLocalization

       - Take parameter: color image.

       - First Step: Find the center
         We first project the image in the vertical and horizontal direction and get an estimated the center (xp,yp) of the pupil by searching the minimum value of two coordinates (lowest row and column sum). Then binarize a region using a threshhold of 64 to localize the pupil by recalculate the center. 

       - Second step: Find circles
         We use Hough transform for detecting the circles for pupil and iris and draw the boundary. Return innerCircle and outterCircle in turple format and both of them contain the x and y coordinate of center and corresponding radius.

#### 2.Funtion name: irisLocalizationDrawing

       - Take parameter: image file name.

       - This function takes the excatly same steps as irisLocalization(). Besides, it also draws the image with two boundaries. Designed for testing, debugging, and visualizing.

### Iris Normalization

#### 1.Function name: getDistance

       - Take parameter: Two data points in the format (x1, y1, x2, y2)
       - Return: The distance between these two points. (will be using as parameter in the function getLongRadius() below.)
       - This funtion will be called in the function getxy() below.

#### 2.Function name: getInverseTan

       - Take parameter: Two data points in the format (x1, y1, x2, y2)
       - Return: The inverse of tangent between two points. (will be using as parameter in the function getLongRadius() below.)
       - This funtion will be called in the function getxy() below.

#### 3.Function name: getLongRadius

       - Take parameter: Distance, outterCircle and the result in getInverseTan() in the format (distance, radius, theta)
       - Return: The radius of the iris, which is longer than the radius of pupil.
       - This funtion will be called in the function getxy() below for calculating the (xi(theta), yi(theta)), which is the coordinate of the outer boundary point in the direction theta in the original image Io.

#### 4.Function name: getxy

       - Take parameter: X, Y, innerCircle and outterCircle that we get from the function irisLocalization()
       - Return: (x,y)
       - In this function, we project the original iris in a Cartesian coordinate system into a doubly dimensionless pseudopolar coordinate by taking the X,Y of the normalized image and finding the corresponding x,y from the round image. This funtion will be called in the function getNormalization() below

#### 5.Function name: getNormalization

       - Take parameter: image,innerCircle,outterCircle
       - Return: new image 
       - For each pixel in normalized image, find the value for the corresponding pixels in the original image by calling the function getxy() and fill in the value.

#### 6.Function name: getRotation ?????

       - Take parameter: image, degree
       - Return: 
       - This function takes normalized image and rotate the rectangle image to specified degree.

### Image Enhancement

#### 1.Function name: enhancement

       - Take parameter: image
       - Return: enhanced image by equalizing the histogram of the image.

#### 2.Function name: imageEnhancementByParts

       - Take parameter: image
       - Return: enhanced image using histogram equalization by 32x32 pixels region.

#### 3.Function name: allEnhancement ?????

       - Take parameter: image
       - Return:

### Feature Extraction

The frequency and orientation information can identify the local spatial patterns of different irises in the texture analysis. Since we normalize the image before, the orientation information among irises will not be the major differences of irises. So in this section, we focus on the frequency information.

#### 1.Function name: roi

       - Take parameter: image
       - Return: Top 48 rows of the image which is the Region Of Interest

#### 2.Function name: m1

       - Take parameter:
       - Return:

#### 3.Function name: g

       - Take parameter:
       - Return:

#### Function name: 

       - Take parameter:
       - Return:


### Iris Matching

### Performance Evaluation

## Result and Limitation
