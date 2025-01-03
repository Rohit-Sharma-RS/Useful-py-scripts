import cv2
import math
import time
import pyautogui
from gesture import handDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = handDetector(detectionCon=0)

smoothening = 7 
prev_hand_x, prev_hand_y = 0, 0
prev_mouse_x, prev_mouse_y = 0, 0
pTime = 0
gesture_text = ""

def is_victory_sign(fingers):
    return fingers == [0, 1, 1, 0, 0]  # Index and middle fingers up

def is_yo_sign(fingers):
    return fingers == [1, 0, 0, 0, 1]  # Thumb and little fingers up

def is_open_hand(fingers):
    return fingers == [1, 1, 1, 1, 1]  # All fingers up

def is_fist(fingers):
    return fingers == [0, 0, 0, 0, 0]  # You get the idea!!

def is_volume_control(fingers):
    return fingers == [0, 1, 0, 0, 1]

def is_left_pinky_click(fingers):
    return fingers == [0, 0, 0, 0, 1]


volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    tipId = [4, 8, 12, 16, 20]  

    if len(lmList) != 0:

        wrist_x = lmList[0][1]
        hand_type = "Right" if wrist_x > wCam // 2 else "Left"

        fingers = []
        if lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, len(tipId)):
            if lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]:
                fingers.append(1)  
            else:
                fingers.append(0)


        if hand_type == "Right":
            if is_victory_sign(fingers):
                pyautogui.scroll(20)
                gesture_text = "Scroll Up (Victory Sign)"
            

            elif is_yo_sign(fingers):
                pyautogui.scroll(-20)
                gesture_text = "Scroll Down (Yo Sign)"

            elif is_open_hand(fingers):
                hand_x, hand_y = lmList[9][1], lmList[9][2]
                direction_x = (prev_hand_x - hand_x) * 20
                direction_y = (hand_y - prev_hand_y) * 20
                screen_width, screen_height = pyautogui.size()
                mouse_x = prev_mouse_x + direction_x
                mouse_y = prev_mouse_y + direction_y
                mouse_x = min(max(0, mouse_x), screen_width)
                mouse_y = min(max(0, mouse_y), screen_height)
                smooth_mouse_x = prev_mouse_x + (mouse_x - prev_mouse_x) / smoothening
                smooth_mouse_y = prev_mouse_y + (mouse_y - prev_mouse_y) / smoothening
                pyautogui.moveTo(smooth_mouse_x, smooth_mouse_y)
                prev_mouse_x, prev_mouse_y = smooth_mouse_x, smooth_mouse_y
                prev_hand_x, prev_hand_y = hand_x, hand_y
                gesture_text = "Mouse Movement (Open Hand)"
            
            elif is_fist(fingers):
                pyautogui.hotkey("click")
                gesture_text = "Click (Fist)"
            
            elif is_volume_control(fingers):
                length = math.hypot(lmList[8][1] - lmList[4][1], lmList[8][2] - lmList[4][2])
                vol = np.interp(length, [50, 300], [minVol, maxVol])
                volBar = np.interp(length, [50, 300], [400, 150])
                volPer = np.interp(length, [50, 300], [0, 100])
                volume.SetMasterVolumeLevel(vol, None)
                gesture_text = "Volume Control"
        
        elif hand_type == "Left":

            if is_open_hand(fingers):
                pyautogui.hotkey("ctrl", "+")
                time.sleep(0.5)
                gesture_text = "Zoom In (Open Hand)"
            
            elif is_fist(fingers):
                pyautogui.hotkey("ctrl", "-")
                time.sleep(0.5)
                gesture_text = "Zoom Out (Fist)"
        
            
            elif is_yo_sign(fingers):
                pyautogui.hotkey("alt", "tab")
                time.sleep(1.5)
                gesture_text = "Switch Application (Inverted Victory Sign)"


        cv2.putText(img, f"{gesture_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        print(gesture_text)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)


    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    img = cv2.flip(img, 1)
    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()