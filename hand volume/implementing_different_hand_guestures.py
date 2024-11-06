import cv2
import math
import time
import pyautogui
from gesture import handDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

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

# Zoom and volume parameters
last_zoom_in_time = time.time()
last_zoom_out_time = time.time()
zoom_cooldown = 0.5
pTime = 0
Percent = 0

# Define gesture recognition functions
def is_victory_sign(fingers):
    return fingers == [0, 1, 1, 0, 0]  # Index and middle fingers up

def is_yo_sign(fingers):
    return fingers == [1, 0, 0, 0, 1]  # Thumb and pinky fingers up

def is_good_sign(fingers):
    return fingers == [0, 0, 1, 1, 1]  # Good sign (middle, ring, and pinky fingers up)

def is_open_hand(fingers):
    return fingers == [1, 1, 1, 1, 1]  # All fingers up

def is_fist(fingers):
    return fingers == [0, 0, 0, 0, 0]  # All fingers down

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    tipId = [4, 8, 12, 16, 20]  # Thumb and finger tips

    # Check if landmarks are detected
    if len(lmList) != 0:
        # Detect if it's the right or left hand based on wrist position
        wrist_x = lmList[0][1]
        hand_type = "Right" if wrist_x > wCam // 2 else "Left"

        # Determine which fingers are up
        fingers = []
        # Thumb check
        if lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]:  # Right of thumb's lower joint
            fingers.append(1)
        else:
            fingers.append(0)

        # Check other fingers (index, middle, ring, pinky)
        for id in range(1, len(tipId)):
            if lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]:  # Above the lower joint
                fingers.append(1)
            else:
                fingers.append(0)

        # Volume control with left hand
        if hand_type == "Left" and fingers[1] == 1 and fingers[0] == 1:  # Thumb and index finger up
            x1, y1 = lmList[8][1:]
            x0, y0 = lmList[4][1:]
            distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            if distance < 50:
                distance = 50
            elif distance > 250:
                distance = 250
            Percent = round((distance - 50.0) / 2)
            Changevolume = round(math.log((Percent / 10) + 1) * 50 * 0.54)
            volume.SetMasterVolumeLevel(-65.25 + Changevolume, None)

        # Zoom control with right hand
        elif hand_type == "Right" and fingers[0] == 1 and fingers[1] == 1:  # Thumb and index finger together
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

        # Recognize and display additional right-hand gestures
        if hand_type == "Left":
            if is_victory_sign(fingers):
                gesture_text = "Victory Sign"
            elif is_yo_sign(fingers):
                gesture_text = "Yo Sign"
            elif is_good_sign(fingers):
                gesture_text = "Good Sign"
            elif is_open_hand(fingers):
                gesture_text = "Open Hand"
            elif is_fist(fingers):
                gesture_text = "Fist"
            else:
                gesture_text = "Gesture Not Recognized"
            
            # Display recognized gesture
            cv2.putText(img, f"{gesture_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            print(gesture_text)  # Print gesture to the console

    # Frame rate display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    # Show video feed
    img = cv2.flip(img, 1)
    cv2.imshow("Gesture Control", img)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
