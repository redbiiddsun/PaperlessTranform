import cv2 
import numpy as np
from matplotlib import pyplot as plt
import re

img_path = "img/example3.jpg" # Image path
img = cv2.imread(img_path)

# Inverted Image
inverted_img = cv2.bitwise_not(img)

# Binarization Image
def grayscale(image): # Gray Scale Function
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_img = grayscale(img)

thresh, img_bw = cv2.threshold(gray_img, 137 , 255, cv2.THRESH_BINARY)

# Noise Removal
def noise_removal(image):
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    # image = cv2.medianBlur(image, 3)
    return (image)

nonoise_img = noise_removal(img_bw)

# Dilation and Erosion
def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

eroded_img = thin_font(nonoise_img)
dilated_img = thick_font(nonoise_img)

plt.imshow(img_bw, cmap="gray")
plt.axis("off")  # Hide axes
plt.show()

# import easyocr
# reader = easyocr.Reader(['th', 'en'])
# result = reader.readtext(img_bw)
# extracted_text = "\n".join([text[1] for text in result])
# print(extracted_text)

import pytesseract
from pytesseract import Output
custom_config = r'-l tha+eng --oem 3 --psm 4 '
data = pytesseract.image_to_string(img,config=custom_config, output_type=Output.DICT)
print(data["text"].replace("\\n", "\n"))
# data = pytesseract.image_to_boxes(img_bw, config=custom_config)
# hImg,wImg = img_bw.shape
# for b in data.splitlines():
#     b = b.split(' ')
#     print(b)
#     x,y,w,h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
#     cv2.rectangle(img_bw,(x,y),(x+w,y+h),(0,0,255),1)

# plt.imshow(img_bw, cmap="gray")
# plt.axis("off")  # Hide axes
# plt.show()