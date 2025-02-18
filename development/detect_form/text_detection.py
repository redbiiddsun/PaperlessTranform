import pytesseract
import cv2
import easyocr
import matplotlib.pyplot as plt


from utils import Utils
class TextDetection:

    def __init__(self):
        pass

    def detect_text(self, image):
        custom_config = r'-l tha --oem 3 --psm 6 --dpi 2400'
        data = pytesseract.pytesseract.image_to_string(image, config=custom_config)
        print(data)

    def easy_ocr(self, image):
        reader = easyocr.Reader(['en', 'th'], gpu=True)
        result = reader.readtext(image, detail = 0, paragraph=False)
        print(result)


tmp = TextDetection().detect_text(Utils().preprocess_image('./image/Medium/1.png'))

