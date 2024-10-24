import numpy as np
import cv2
import math 
import time
from gesture import handDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import math

# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
currentVolumeDb = volume.GetMasterVolumeLevel()

wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Set width of the camera
cap.set(4, hCam)  # Set height of the camera
detector = handDetector(detectionCon=0.75)

LastPx = 800
LastPy = 0
Percent = 0
zoom_factor = 1.0

while True:
    success, img = cap.read()  # Read the camera frame
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    tipId = [4, 8, 12, 16, 20] # Thumb, Index finger, middle finger, ring finger, pinky finger

    if len(lmList) != 0:
        fingers = []
        # Thumb: If thumb is to the right of the hand, it's a right hand
        if lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # Other four fingers
        for id in range(1, len(tipId)):
            if lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                
        # Detect zoom gesture (using left hand)
        if fingers[1] == 1 and fingers[0] == 1:
            x1, y1 = lmList[8][1:]  # Index finger tip
            x0, y0 = lmList[4][1:]  # Thumb tip
            
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x0, y0), 15, (0, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x0, y0), (0, 0, 255), 2)
            
            # Calculate distance between thumb and index finger
            distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            
            # Zoom factor scaling
            zoom_factor = 1.0 + (distance - 50) / 200.0
            zoom_factor = min(max(zoom_factor, 1.0), 2.0)  # Limit zoom to 1.0x - 2.0x

            # Implement zoom effect on the image
            h, w, c = img.shape
            centerX, centerY = w // 2, h // 2
            new_w, new_h = int(w / zoom_factor), int(h / zoom_factor)
            img = img[centerY - new_h // 2:centerY + new_h // 2, centerX - new_w // 2:centerX + new_w // 2]
            img = cv2.resize(img, (w, h))
            
            # Update volume based on the same hand gesture logic
            if distance < 50:
                distance = 50
            elif distance > 250:
                distance = 250
            Percent = round((distance - 50.0) / 2)

            Changevolume = round(math.log((Percent / 10) + 1) * 50 * 0.54)
            volume.SetMasterVolumeLevel(-65.25 + Changevolume, None)
    
    # Display volume bar
    height = int(340 - (Percent * 2.0))
    cv2.rectangle(img, (570, height), (620, 340), (0, 255, 0), -1)
    cv2.rectangle(img, (570, 140), (620, 340), (255, 0, 0), 2)
    
    # Display zoom level on the screen
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (15, 130)
    fontScale = 1
    fontColor = (0, 0, 0)
    lineType = 2
    cv2.putText(img, f'Zoom: {zoom_factor:.2f}x', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

    # Calculate FPS
    cTime = time.time()
    fps = 1.0 / float(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), font, fontScale, (0, 0, 255), 2)

    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
