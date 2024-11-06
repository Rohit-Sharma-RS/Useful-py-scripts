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
cap.set(3, wCam)
cap.set(4, hCam)
detector = handDetector(detectionCon=0)
detector = handDetector(detectionCon=1)
Percent = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    tipId = [4, 8, 12, 16, 20]
    
    if len(lmList) != 0:
        fingers = []

        # Thumb check
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

            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x0, y0), 15, (0, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x0, y0), (0, 0, 255), 2)

            # Calculate the distance between the index and thumb
            distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

            # Limit distance values for volume control
            if distance < 50:
                distance = 50
            elif distance > 250:
                distance = 250

            # Convert distance to percentage for volume control
            Percent = round((distance - 50.0) / 2)

            # Calculate the change in volume
            Changevolume = round(math.log((Percent / 10) + 1) * 50 * 0.54)
            volume.SetMasterVolumeLevel(-65.25 + Changevolume, None)

    # Draw volume bar
    height = int(340 - (Percent * 2.0))
    cv2.rectangle(img, (570, height), (620, 340), (0, 255, 0), -1)
    cv2.rectangle(img, (570, 140), (620, 340), (255, 0, 0), 2)

    # Frame rate calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display frame rate on the image
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display the result frame
    cv2.imshow("Volume Control", img)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
