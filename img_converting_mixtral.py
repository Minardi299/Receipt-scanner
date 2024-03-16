
import cv2
import pytesseract
from PIL import Image
import numpy as np
# Load the receipt image
img = cv2.imread('TestingImgs/test1.jpeg')
def remove_borders(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    contours, heiarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = img[y:y+h, x:x+w]
    return (crop)

def thickening_font(img: np.ndarray) -> np.ndarray:
    img=cv2.bitwise_not(img)
    kernel=np.ones((2,2),np.uint8)
    img=cv2.dilate(img,kernel,iterations=1)
    img=cv2.bitwise_not(img)
    return img
def get_boxes(img):
    h, w = img.shape
    boxes = pytesseract.image_to_boxes(img) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    return img

def noise_removal(image: np.ndarray):
    kernel = np.ones((1,1),np.uint8)
    image=cv2.dilate(image,kernel,iterations=1)
    kernel=np.ones((1,1),np.uint8)
    image=cv2.erode(image,kernel,iterations=1)
    image=cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernel)
    image=cv2.medianBlur(image,3)
    return (image)
img = remove_borders(img)
# Convert to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

# Use adaptive thresholding to binarize the image
# thresh_img = cv2.adaptiveThreshold(no_noise, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 5)
thresh_img = cv2.adaptiveThreshold(blurred_img, 210, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 10)
# thresh_img = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 15)
no_noise = noise_removal(thresh_img)
# Remove borders and unwanted elements using morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
cleaned_img = cv2.morphologyEx(no_noise, cv2.MORPH_OPEN, kernel)

# Resize the image to improve Tesseract's ability to recognize text
resized_img = cv2.resize(cleaned_img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
thick_font = thickening_font(resized_img)
# Use PIL to convert resized image to a format that Tesseract can read
# pil_img = Image.fromarray(resized_img)

# Use Tesseract to extract text from the preprocessed image
# box=get_boxes(thick_font)
cv2.imwrite("processed/mixtralemoveNoise.jpg", thick_font)
text = pytesseract.image_to_string(thick_font, lang='eng', config='--psm 6')
destination_path = f"Result/mixtral.txt"
with open(destination_path,'w') as file:
    file.write(text)
