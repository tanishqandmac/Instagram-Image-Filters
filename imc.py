import cv2
from PIL import Image
import numpy as np
import cv2
import argparse

#sourceFile = 's1.jpg'
#targetFile = 't1.jpg'

def converter(a,t_Mean,t_StandardDeviation,s_StandardDeviation,s_Mean):
    a = a - t_Mean
    a = (t_StandardDeviation/s_StandardDeviation)*a
    a = a + s_Mean
    a = np.clip(a,0,255)
    return a

def imgStyleTransfer(sourceFileName, targetFileName):
    sourceFileName = cv2.cvtColor(sourceFileName, cv2.COLOR_BGR2LAB).astype("float32")
    targetFileName = cv2.cvtColor(targetFileName, cv2.COLOR_BGR2LAB).astype("float32")
    (l,a,b) = cv2.split(targetFileName)
    (sourceMeanL,sourceStandardDeviationL,sourceMeanA,sourceStandardDeviationA,sourceMeanB,sourceStandardDeviationB) = imgStatisticalComputation(sourceFileName)
    (targetMeanL,targetStandardDeviationL,targetMeanA,targetStandardDeviationA,targetMeanB,targetStandardDeviationB) = imgStatisticalComputation(targetFileName)
    
    a = converter(a,targetMeanA,targetStandardDeviationA,sourceStandardDeviationA,sourceMeanA)
    b = converter(b,targetMeanB,targetStandardDeviationB,sourceStandardDeviationB,sourceMeanB)
    l = converter(l,targetMeanL,targetStandardDeviationL,sourceStandardDeviationL,sourceMeanL)

    transfer = cv2.merge([l,a,b])
    transfer = cv2.cvtColor(transfer.astype("uint8"),cv2.COLOR_LAB2BGR)
    return transfer

def imgIncreaseBrightness(img,value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    lim = 255 - value
    v[v>lim] = 255
    v[v<=lim] =v[v<=lim] + value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def imgStatisticalComputation(image):
    (l,a,b) = cv2.split(image)
    (mean_L,StandardDeviation_L) = (l.mean(),l.std())
    (mean_A,StandardDeviation_A) = (a.mean(),a.std())
    (mean_B,StandardDeviation_B) = (b.mean(),b.std())
    return (mean_L,StandardDeviation_L,mean_A,StandardDeviation_A,mean_B,StandardDeviation_B)

def saveImage(image):
    width=720
    r = width/float(image.shape[1])
    dim = (width,int(image.shape[0]*r))
    resized = cv2.resize(image,dim,interpolation=cv2.INTER_AREA)
    cv2.imwrite("Output/Style Transfer.jpg",resized)

#Preprocessing and Reading the Image
sourceImage = raw_input("Enter Image name for Task 1, 2 & 3:")
img_1 = cv2.imread(sourceImage + '.jpg',3)
img_2 = 255 - img_1
im1 = Image.open(sourceImage + '.jpg')
brightness = raw_input("Enter Amount of Brightness (0-100%) :")
brightnessScaled = (float(brightness)/100.0)*255
darkness = raw_input("Enter Amount of Darkness (0-100%) :")
darknessScaled = 1 - (float(darkness)/100.0)
print "Images from Task 1, Task 2 and Task 3 saved in Output folder"
print "\n"
print "Task 4".center(50,'-')
newSourceFile = raw_input("Enter name of Source File:")
newTargetFile = raw_input("Enter name of Target File:")
print "\n"

#Performing Task 1
cv2.imwrite('Output/Negative Image.jpg',img_2)

#Performing Task 2
img_3 = imgIncreaseBrightness(img_1,int(brightnessScaled))
cv2.imwrite('Output/Brightened Image.jpg',img_3)

#Performing Task 3
im1.point(lambda p: p * darknessScaled).save('Output/Darkened Image.jpg')

#Performing Task 4
#Importing Source and Target Images
source = cv2.imread(newSourceFile + '.jpg')
target = cv2.imread(newTargetFile + '.jpg')
#Image Style Transfer
transfer = imgStyleTransfer(source, target)
saveImage(transfer)

print " All Tasks Completed ".center(50,"#")
