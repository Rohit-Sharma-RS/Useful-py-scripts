import cv2
import math
import time
import pyautogui
from gesture import handDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
import speech_recognition as sr
from deepface import DeepFace
import simple_colors
from helper_functions import send_message, search_google, play_music_spotify, play_music_youtube, AI_modify, my_sentiment_analyzer, recommender_AI

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
switch_app_flag = False

def is_victory_sign(fingers):
    return fingers == [0, 1, 1, 0, 0]

def is_yo_sign(fingers):
    return fingers == [1, 0, 0, 0, 1]

def is_open_hand(fingers):
    return fingers == [0, 1, 0, 0, 0]

def is_thumb(fingers):
    return fingers == [1, 0, 0, 0, 0]

def is_bad(fingers):
    return fingers == [0, 0, 1, 0, 0]

def is_fist(fingers):
    return fingers == [0, 0, 0, 0, 0]

def is_volume_control(fingers):
    return fingers == [0, 1, 0, 0, 1]

def is_left_pinky_click(fingers):
    return fingers == [0, 0, 0, 0, 1]

def is_four_fingers(fingers):
    return fingers == [0, 1, 1, 1, 1]

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

recognizer = sr.Recognizer()

def recognize_speech():
    print("Listening for speech...")
    with sr.Microphone() as source:
        print(simple_colors.red("Adjusting for ambient noise..."))
        recognizer.adjust_for_ambient_noise(source, duration=0.7)
        print(simple_colors.green("Calibration complete, start speaking..."))
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)

            if "instagram" in text.lower() or "insta" in text.lower():
                text = text.replace("Instagram", "").replace("message", "").strip()
                text = AI_modify(text)
                send_message(text)

            elif "google" in text.lower() or "search" in text.lower():
                text = text.replace("Google", "").replace("search", "").strip()
                text = AI_modify(text)
                search_google(text)

            elif "spotify" in text.lower():
                text = text.replace("play", "").replace("spotify", "").strip()
                text = AI_modify(text)

                if "recommend" in text.lower():
                    text = recommender_AI(text)

                play_music_spotify(text)

            elif "YouTube" in text.lower():
                text = text.replace("play", "").replace("YouTube", "").strip()
                text = AI_modify(text)
                play_music_youtube(text)

            else:
                print(f"You said {text}")
                sentiment_analyze = my_sentiment_analyzer(text)
                print(sentiment_analyze)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error with the Speech Recognition service: {e}")
        except sr.WaitTimeoutError:
            print("Speech recognition timed out.")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=True)
    lmList=[]
    lmList = detector.findPosition(img, draw=False)
    tipId = [4, 8, 12, 16, 20]

    if len(lmList) == 0:
        results = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        dominant_emotion = results[0]['dominant_emotion'] if isinstance(results, list) else results['dominant_emotion']

        if dominant_emotion in ["angry", "fear"]:
            dominant_emotion = "neutral"

        if dominant_emotion != 'happy':
            cv2.putText(img, "The camera is looking at you just smile [ o*]!", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        else:
            cv2.putText(img, "Oh I detect a smile :) !", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(img, f"Detected Emotion: {dominant_emotion}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

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
                pyautogui.scroll(35)
                gesture_text = "Scroll Up (Victory Sign)"

            elif is_bad(fingers):
                gesture_text = "Don't show that finger"

            elif is_yo_sign(fingers):
                pyautogui.scroll(-30)
                gesture_text = "Scroll Down (Yo Sign)"

            elif is_open_hand(fingers):
                hand_x, hand_y = lmList[8][1], lmList[8][2]
                direction_x = (hand_x - prev_hand_x) * 30
                direction_y = (hand_y - prev_hand_y) * 30
                current_mouse_x, current_mouse_y = pyautogui.position()
                mouse_x = current_mouse_x + direction_x
                mouse_y = current_mouse_y + direction_y
                screen_width, screen_height = pyautogui.size()
                mouse_x = min(max(0, mouse_x), screen_width)
                mouse_y = min(max(0, mouse_y), screen_height)
                smooth_mouse_x = current_mouse_x + (mouse_x - current_mouse_x) / smoothening
                smooth_mouse_y = current_mouse_y + (mouse_y - current_mouse_y) / smoothening
                pyautogui.moveTo(smooth_mouse_x, smooth_mouse_y)
                prev_hand_x, prev_hand_y = hand_x, hand_y
                gesture_text = "Mouse Movement (Index Finger)"

            elif is_fist(fingers):
                pyautogui.click()
                gesture_text = "Click (Fist)"

            elif is_volume_control(fingers):
                min_dist = 60  # Minimum distance for the lowest volume
                max_dist = 100  # Maximum distance for the highest volume

                length = math.dist((lmList[8][1], lmList[8][2]), (lmList[4][1], lmList[4][2]))

                vol = np.interp(length, [min_dist, max_dist], [minVol, maxVol])

                volBar = np.interp(length, [min_dist, max_dist], [400, 150])
                volPer = np.interp(length, [min_dist, max_dist], [0, 100])

                volume.SetMasterVolumeLevel(vol, None)

                gesture_text = "Volume Control"

        elif hand_type == "Left":
            if is_open_hand(fingers):
                pyautogui.hotkey("ctrl", "+")
                gesture_text = "Zoom In"
                time.sleep(0.5)

            elif is_fist(fingers):
                pyautogui.hotkey("ctrl", "-")
                gesture_text = "Zoom Out (Fist)"
                time.sleep(0.5)

            elif is_four_fingers(fingers):
                if not switch_app_flag:
                    pyautogui.hotkey("alt", "tab")
                    gesture_text = "Switch Application"
                    switch_app_flag = True
                else:
                    switch_app_flag = False

            elif is_left_pinky_click(fingers):
                recognize_speech()
                gesture_text = "Speech Recognition (Pinky Up)"
            
            elif is_thumb(fingers):
                recognize_speech()
                gesture_text = "Speech Recognition (Thumb Up)"

            elif is_bad(fingers):
                gesture_text = "Closing application"
                pyautogui.hotkey("alt", "f4")
                pyautogui.hotkey("q")

        cv2.putText(img, f"{gesture_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
