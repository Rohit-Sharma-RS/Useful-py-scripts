import easyocr
import cv2

reader = easyocr.Reader(['en'])
image_path = 'screenshot.png'
image = cv2.imread(image_path)

results = reader.readtext(image)

for bbox, text, prob in results:
    print(f"Detected text: {text} (Confidence: {prob:.2f})")
