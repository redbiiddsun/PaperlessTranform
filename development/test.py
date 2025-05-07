import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np

# Convert PDF to images
pdf_path = './file/dot_input/Complain.pdf'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r'C:\Users\Pra_p\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'

images = convert_from_path(pdf_path, poppler_path=poppler_path)

for page_num, image in enumerate(images):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours for checkboxes
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    checkbox_regions = []
    options = []
    
    # Get image dimensions
    img_height, img_width = img.shape[:2]
    min_size = 0.01
    max_size = 0.05
    
    min_w = img_width * min_size
    max_w = img_width * max_size
    min_h = img_height * min_size
    max_h = img_height * max_size

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        area = cv2.contourArea(cnt)
        
        if (min_w <= w <= max_w and min_h <= h <= max_h) and (0.3 <= aspect_ratio <= 3.0) and area > 500:
            checkbox_regions.append((x, y, w, h))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Extract option text next to the checkbox
            option_x = x + w
            option_y = y - 10
            option_w = 200
            option_h = h + 10

            option_roi = gray[option_y:option_y+option_h, option_x:option_x+option_w]
            option_text = pytesseract.image_to_string(option_roi, lang='tha', config='--psm 6')

            # Postprocessing: Strip spaces and check for whitespace between characters
            options.append(option_text.strip())

    # OCR extraction for full page
    extracted_text = pytesseract.image_to_string(gray, lang='tha', config='--psm 6') 

    print("Extracted text:", extracted_text)
    print("Detected Checkboxes:", checkbox_regions)
    print(f"Number of detected checkboxes: {len(checkbox_regions)}")
    print("Detected options:")
    for idx, option in enumerate(options):
        print(f"Option {idx + 1}: {option}")

    # Show detected checkboxes on the image
    cv2.imshow(f'Page {page_num + 1}', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
