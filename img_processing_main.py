import cv2
import numpy as np
import pytesseract
from chatopenai import *


def thickening_font(img: np.ndarray) -> np.ndarray:
    img=cv2.bitwise_not(img)
    kernel=np.ones((2,2),np.uint8)
    img=cv2.dilate(img,kernel,iterations=1)
    img=cv2.bitwise_not(img)
    return img

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((1,1),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((1,1),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def get_boxes(img):
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    return img


#The best result so far
def process_img(img: np.ndarray) -> np.ndarray:
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.adaptiveThreshold(img, 210, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 10)
    img = remove_noise(img)
    img=thickening_font(img)
    return img

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

def img_to_string(img: np.ndarray) -> str:
    processed_img = process_img(img)
    text =convert_json(pytesseract.image_to_string(processed_img))
    return text

if __name__ == '__main__':

    #IMG_20231219_1836282
    #IMG_20240316_002532
    img=cv2.imread('TestingImgs/test1.jpeg')
    fixed = process_img(img)
    cv2.imwrite("processed/test2.jpg", fixed)


    text =pytesseract.image_to_string(fixed)
    # print (text)
    print(convert_json(text))

    # destination_path = f"Result/NANO.txt"
    # with open(destination_path,'w') as file:
    #     file.write(text)
