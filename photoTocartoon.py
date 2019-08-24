import os
import cv2
import numpy as np

def turn2cartoon(img_path,save_path):
    path=r'./static/photo/{}'.format(img_path)
    img=cv2.imread(path)
    for i in range(2):
        img=cv2.pyrDown(img)
    for i in range(7):
        img=cv2.bilateralFilter(img,d=9,sigmaColor=9,sigmaSpace=7)
    for i in range(2):
        img=cv2.pyrUp(img)
    #step2
    img_gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    img_blur=cv2.medianBlur(img_gray,7)
    #step3
    img_edg=cv2.adaptiveThreshold(img_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,2)
    #step4
    img_edg=cv2.cvtColor(img_edg,cv2.COLOR_GRAY2BGR)
    img_cartoon=cv2.bitwise_and(img,img_edg)
    cv2.imwrite(path,img_cartoon)
