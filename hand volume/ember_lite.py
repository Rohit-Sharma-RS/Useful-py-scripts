import math
import time
import pyautogui
from gesture import handDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
import cv2

# Set up audio control (PyCAW) for volume adjustment
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Camera dimensions
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = handDetector(detectionCon=0)

# Mouse movement parameters
smoothening = 7
prev_mouse_x, prev_mouse_y = 0, 0
pTime = 0

# Volume control parameters
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Correct mirrored view
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        # Index finger for mouse movement
        index_tip_x, index_tip_y = lmList[8][1], lmList[8][2]
        screen_width, screen_height = pyautogui.size()

        # Map finger coordinates to screen size
        smooth_mouse_x = np.interp(index_tip_x, [0, wCam], [0, screen_width])
        smooth_mouse_y = np.interp(index_tip_y, [0, hCam], [0, screen_height])

        # Smooth mouse movements
        smooth_mouse_x = prev_mouse_x + (smooth_mouse_x - prev_mouse_x) / smoothening
        smooth_mouse_y = prev_mouse_y + (smooth_mouse_y - prev_mouse_y) / smoothening

        pyautogui.moveTo(smooth_mouse_x, smooth_mouse_y)
        prev_mouse_x, prev_mouse_y = smooth_mouse_x, smooth_mouse_y

        # Volume control with index and pinky fingers
        if lmList[4][1:] and lmList[8][1:]:  # Ensure both points exist
            index_pinky_distance = math.dist(lmList[4][1:], lmList[8][1:])
            vol = np.interp(index_pinky_distance, [10, 50], [minVol, maxVol])  # Small movement range
            volBar = np.interp(index_pinky_distance, [10, 50], [400, 150])
            volPer = np.interp(index_pinky_distance, [10, 50], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)

    # Display volume bar and percentage
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # Frame rate display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    # Show the processed video feed
    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
