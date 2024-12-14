import cv2
import math
import time
from gesture import handDetector
import pyautogui

wCam, hCam = 640, 480

zoom_cooldown = 0.5  # Half a second cooldown
    
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = handDetector(detectionCon=0)

last_zoom_in_time = time.time()
last_zoom_out_time = time.time()

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        thumb_x, thumb_y = lmList[4][1], lmList[4][2]
        index_x, index_y = lmList[8][1], lmList[8][2]

        distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

        cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 3)

        if distance > 200 and time.time() - last_zoom_in_time > zoom_cooldown:
            print("Zoom In Gesture Detected!")
            pyautogui.hotkey('ctrl', '+')  
            last_zoom_in_time = time.time()  

        elif distance < 50 and time.time() - last_zoom_out_time > zoom_cooldown:
            print("Zoom Out Gesture Detected!")
            pyautogui.hotkey('ctrl', '-')  
            last_zoom_out_time = time.time() 


    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
