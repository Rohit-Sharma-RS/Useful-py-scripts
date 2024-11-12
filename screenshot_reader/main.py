import time
from PIL import ImageGrab
import pytesseract
import pyttsx3
import keyboard

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if needed

engine = pyttsx3.init()

def capture_and_read():
    screenshot = ImageGrab.grab()

    text = pytesseract.image_to_string(screenshot)

    if text.strip():
        print("Detected text:", text)
        
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    print("Starting screen reader...")

    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Stopping screen reader...")
                break
            capture_and_read()
            time.sleep(5) 

    except KeyboardInterrupt:   
        print("Screen reader stopped.")
