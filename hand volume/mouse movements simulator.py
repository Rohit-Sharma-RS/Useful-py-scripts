import cv2
import math
import time
import numpy as np
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

# Mouse movement parameters
smoothening = 7  # Higher values for more smoothing
prev_hand_x, prev_hand_y = 0, 0
prev_mouse_x, prev_mouse_y = 0, 0
pTime = 0
Percent = 0

# Define gesture recognition functions
def is_victory_sign(fingers):
    return fingers == [0, 1, 1, 0, 0]  # Index and middle fingers up

def is_inverted_victory_sign(fingers):
    return fingers == [0, 0, 1, 1, 0]  # Ring and pinky fingers up

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

        # Volume control with right hand using thumb and index finger
        if hand_type == "Right" and ((fingers[1] == 1 and fingers[0] == 1) or (fingers[3] == 1 and fingers[4] == 1)):
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
            gesture_text = "Volume Control"

        # Left hand mouse control and actions
        elif hand_type == "Left":
            # Mouse pointer movement with open hand
            if is_open_hand(fingers):
                # Use middle finger as a reference point for hand position
                hand_x, hand_y = lmList[9][1], lmList[9][2]  
                
                # Calculate the direction of movement and scale it for faster response
                direction_x = (prev_hand_x - hand_x) * 20  # Scale up the speed
                direction_y = (hand_y - prev_hand_y) * 20  # Scale up the speed

                # Get screen dimensions
                screen_width, screen_height = pyautogui.size()
                
                # Calculate new mouse position
                mouse_x = prev_mouse_x + direction_x
                mouse_y = prev_mouse_y + direction_y

                # Constrain the mouse position within the screen bounds
                mouse_x = min(max(0, mouse_x), screen_width)
                mouse_y = min(max(0, mouse_y), screen_height)

                # Smooth the movement by gradually updating position
                smooth_mouse_x = prev_mouse_x + (mouse_x - prev_mouse_x) / smoothening
                smooth_mouse_y = prev_mouse_y + (mouse_y - prev_mouse_y) / smoothening
                pyautogui.moveTo(smooth_mouse_x, smooth_mouse_y)

                # Update previous positions
                prev_mouse_x, prev_mouse_y = smooth_mouse_x, smooth_mouse_y
                prev_hand_x, prev_hand_y = hand_x, hand_y
                gesture_text = "Mouse Movement (Open Hand)"

            # Left hand mouse click with fist gesture
            elif is_fist(fingers):
                pyautogui.click()
                gesture_text = "Mouse Click (Fist)"

            # Scroll up with victory sign
            elif is_victory_sign(fingers):
                pyautogui.scroll(10)
                gesture_text = "Scroll Up (Victory Sign)"

            # Scroll down with inverted victory sign
            elif is_inverted_victory_sign(fingers):
                pyautogui.scroll(-10)
                gesture_text = "Scroll Down (Inverted Victory Sign)"
            
            # Display recognized gesture
            cv2.putText(img, f"{gesture_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            print(gesture_text)  # Print the gesture to the console

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
