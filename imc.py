import cv2
import numpy
from PIL import Image

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def increase_darkness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

#Reading the Image
img_1 = cv2.imread('mammogram.jpg',3)
img_2 = 255 - img_1
im1 = Image.open("mammogram.jpg")

#Performing Task 1
cv2.imwrite('Output/Negative Image.jpg',img_2)

#Performing Task 2
img_3 = increase_brightness(img_1,0)
cv2.imwrite('Output/Brightened Image.jpg',img_3)

#Performing Task 3
im1.point(lambda p: p * 0.4).save('Output/Darkened Image.jpg')

#Performing Task 4


#5 Second Wait & Close
cv2.waitKey(5000)
cv2.destroyAllWindows()