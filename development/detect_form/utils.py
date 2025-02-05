import cv2
import numpy as np
from skimage.restoration import richardson_lucy

class Utils():

    def __init__(self):
        pass

    def preprocess_image(self, path):
        # Load the image
        image = cv2.imread(path)


        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        # Apply sharpening using Unsharp Masking
        gaussian_blur = cv2.GaussianBlur(gray_image, (0, 0), 3)
        sharpened = cv2.addWeighted(gray_image, 1.5, gaussian_blur, -0.5, 0)


        # Apply contrast enhancement using CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(sharpened.astype(np.uint8))

        return enhanced



