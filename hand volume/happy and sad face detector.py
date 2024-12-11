import os
import cv2
import math
import time
import pyautogui
from gesture import handDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
from deepface import DeepFace

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings

# Set up audio control (PyCAW) for volume adjustment
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Camera dimensions
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = handDetector(detectionCon=0)  # Higher detection confidence
smoothening = 7
gesture_text = ""

# Volume control parameters
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volBar = 400
volPer = 0

def is_victory_sign(fingers):
    return fingers == [0, 1, 1, 0, 0]

def is_volume_control(fingers):
    return fingers == [0, 1, 0, 0, 1]

# Emotion detection phase
emotion_detected = False
while not emotion_detected:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror the frame

    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = results[0]['dominant_emotion'] if isinstance(results, list) else results['dominant_emotion']

        if dominant_emotion != 'happy':
            cv2.putText(frame, "You do not look very happy today.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(frame, "The camera is looking at you just smile[ ◉¯]!", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow("Emotion Detector", frame)

        else:
            cv2.putText(frame, "Oh I detect a beautiful smile!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            time.sleep(1)
            emotion_detected = True

        cv2.putText(frame, f"Detected Emotion: {dominant_emotion}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    except Exception as e:
        cv2.putText(frame, "Face not detected. Please look at the camera.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Emotion Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Start gesture detection phase
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    tipId = [4, 8, 12, 16, 20]

    if len(lmList) != 0:
        fingers = []
        if lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]:
            fingers.append(1)  # Thumb
        else:
            fingers.append(0)

        for id in range(1, len(tipId)):
            if lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if is_victory_sign(fingers):
            pyautogui.scroll(35)
            gesture_text = "Scroll Up (Victory Sign)"
        elif is_volume_control(fingers):
            length = math.dist((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]))
            vol = np.interp(length, [20, 100], [minVol, maxVol])
            volBar = np.interp(length, [20, 100], [400, 150])
            volPer = np.interp(length, [20, 100], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)
            gesture_text = "Volume Control"

        cv2.putText(img, f"{gesture_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    img = cv2.flip(img, 1)
    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
