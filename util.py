import cv2
import numpy as np
def yellow_mask(image):
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv,np.asarray([20,100,150]),np.asarray([60,255,255]))
    return color_mask

def red_mask(image):
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    first = cv2.inRange(hsv,np.asarray([0,50,50]),np.asarray([15,255,255]))
    second = cv2.inRange(hsv,np.asarray([170,50,50]),np.asarray([180,255,255]))
    color_mask = cv2.bitwise_or(first,second)
    return color_mask

def roi_yellow(image):
    crop = image[220:240,150:170]
    return crop

def roi_red(image):
    kernel = np.ones((5,5),np.uint8)
    crop = image[2:5,0:320]
    erode = cv2.erode(crop,kernel,iterations=1)
    return erode

def max_value(image):
    value, count = np.unique(image,return_counts=True)
    ind = np.argmax(count)
    return bool(value[ind])

def count_white(image):
    count = np.sum(image == 255)
    return bool(count)
