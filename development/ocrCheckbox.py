import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np
import json
import re

# Convert PDF to images
pdf_path = './file/dot_input/แบบฟอร์มผู้ป่วยใหม่.pdf'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r'C:\Users\Pra_p\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'

images = convert_from_path(pdf_path, poppler_path=poppler_path)

for page_num, image in enumerate(images):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_height, img_width = img.shape[:2]
    # Apply adaptive thresholding for better text contrast
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    rebinary = cv2.bitwise_not(binary)

    # Denoising the image to improve OCR accuracy
    binary = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)

    # Find contours for checkboxes
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    checkbox_data = []  # To store checkbox and option details

    # Get image dimensions
    min_size = 0.01
    max_size = 0.1
    min_w = img_width * min_size
    max_w = img_width * max_size
    min_h = img_height * min_size
    max_h = img_height * max_size
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        area = cv2.contourArea(cnt)

        roi = (rebinary[y:y + 10, x:x + 10])
        if (min_w <= w <= max_w and min_h <= h <= max_h) and (0.8 < aspect_ratio < 1.2) and 100 < area < 1000 and 11 < np.sum(roi)/1000 < 16.8 :
            print(f"w,h: {w,h} ratio: {aspect_ratio}Area: {area} Roi : {np.sum(roi)/1000}")
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Extract option text next to the checkbox
            option_x = x + w
            option_y = y - 5
            option_w = 300
            option_h = h + 10

            option_roi = gray[option_y:option_y + option_h, option_x:option_x + option_w]

            # Use a higher DPI or try adjusting the OCR mode (psm)
            option_text = pytesseract.image_to_string(option_roi, lang='tha', config='--psm 6 --oem 3').split(' ')[0]

            # Clean option text (remove extra spaces, brackets, and symbols)
            clean_option_text = re.sub(r'[\[\]\"\'\s]+', ' ', option_text).strip()
            print(f"Text: {clean_option_text}")
            # Check if the option text is likely a valid string and not a box
            if len(clean_option_text) > 0:
                checkbox_data.append({
                    "option": clean_option_text,
                    "position": f"{x}, {y}, {w}, {h}"
                })

            # Draw a rectangle around the option text
            cv2.rectangle(img, (option_x, option_y), (option_x + option_w, option_y + option_h), (255, 0, 0), 2)
            
    # Output in JSON format
    json_output = {
            "Detected Checkboxes": checkbox_data,
            "Number of detected checkboxes": len(checkbox_data)
        }
    print(json.dumps(json_output, ensure_ascii=False, indent=4))

    # Show detected checkboxes and options on the image 
    scale_factor = 0.5 # You can adjust this value to change the size
    resized_img = cv2.resize(img, (int(img_width * scale_factor), int(img_height * (scale_factor-0.1))))

    # Show resized image
    cv2.imshow(f'Page {page_num + 1}', resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

