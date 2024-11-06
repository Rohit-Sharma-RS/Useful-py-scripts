import cv2
import math
import time
from gesture import handDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pyautogui

# Set up audio control (PyCAW) for volume adjustment
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Camera dimensions
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = handDetector(detectionCon=1)

# Volume and zoom parameters
last_zoom_in_time = time.time()
last_zoom_out_time = time.time()
zoom_cooldown = 0.5  # Cooldown time for zoom
pTime = 0
Percent = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    tipId = [4, 8, 12, 16, 20]  # Thumb and finger tips

    # Check if landmarks are detected
    if len(lmList) != 0:
        # Determine if left or right hand (using landmarks position)
        wrist_x = lmList[0][1]
        hand_type = "Right" if wrist_x > wCam // 2 else "Left"

        # Left hand for volume control
        if hand_type == "Left":
            fingers = []
            # Thumb check for left hand
            if lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Check other fingers (index, middle, ring, pinky)
            for id in range(1, len(tipId)):
                if lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Volume control gesture: Thumb and index finger are up
            if fingers[1] == 1 and fingers[0] == 1:
                x1, y1 = lmList[8][1:]
                x0, y0 = lmList[4][1:]
                distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

                # Limit distance values for volume control
                if distance < 50:
                    distance = 50
                elif distance > 250:
                    distance = 250

                Percent = round((distance - 50.0) / 2)
                Changevolume = round(math.log((Percent / 10) + 1) * 50 * 0.54)
                volume.SetMasterVolumeLevel(-65.25 + Changevolume, None)

                # Display volume bar on left side of screen
                height = int(340 - (Percent * 2.0))
                cv2.rectangle(img, (570, height), (620, 340), (0, 255, 0), -1)
                cv2.rectangle(img, (570, 140), (620, 340), (255, 0, 0), 2)

        # Right hand for zoom control
        elif hand_type == "Right":
            # Thumb and index finger coordinates
            thumb_x, thumb_y = lmList[4][1], lmList[4][2]
            index_x, index_y = lmList[8][1], lmList[8][2]
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

            # Draw line for visual feedback
            cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 3)

            # Zoom gestures
            if distance > 200 and time.time() - last_zoom_in_time > zoom_cooldown:
                print("Zoom In Gesture Detected!")
                pyautogui.hotkey('ctrl', '+')
                last_zoom_in_time = time.time()

            elif distance < 50 and time.time() - last_zoom_out_time > zoom_cooldown:
                print("Zoom Out Gesture Detected!")
                pyautogui.hotkey('ctrl', '-')
                last_zoom_out_time = time.time()

    # Frame rate display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Show video feed
    img = cv2.flip(img, 1)
    cv2.imshow("Hand Gesture Control", img)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
