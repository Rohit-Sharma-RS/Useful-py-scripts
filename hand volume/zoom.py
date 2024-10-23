import cv2
import math
import time
from gesture import handDetector
import pyautogui  # Library for simulating key presses

# Camera dimensions
wCam, hCam = 640, 480

# Cooldown time between zoom actions (in seconds)
zoom_cooldown = 1  # 1 second cooldown
    
# Set up video capture and hand detector
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = handDetector(detectionCon=1)

# Time trackers for zoom cooldown
last_zoom_in_time = time.time()
last_zoom_out_time = time.time()

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    # Check if hand landmarks are detected
    if len(lmList) != 0:
        # Thumb and index finger coordinates
        thumb_x, thumb_y = lmList[4][1], lmList[4][2]
        index_x, index_y = lmList[8][1], lmList[8][2]

        # Calculate distance between thumb and index finger
        distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

        # Draw a line between thumb and index finger
        cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 3)

        # Trigger zoom-in if fingers are spread wide (distance > 200)
        if distance > 200 and time.time() - last_zoom_in_time > zoom_cooldown:
            print("Zoom In Gesture Detected!")
            pyautogui.hotkey('ctrl', '+')  # Simulate Ctrl + Plus for zoom in
            last_zoom_in_time = time.time()  # Reset zoom-in time

        # Trigger zoom-out if fingers are pinched together (distance < 50)
        elif distance < 50 and time.time() - last_zoom_out_time > zoom_cooldown:
            print("Zoom Out Gesture Detected!")
            pyautogui.hotkey('ctrl', '-')  # Simulate Ctrl + Minus for zoom out
            last_zoom_out_time = time.time()  # Reset zoom-out time

    # Display the video feed
    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
