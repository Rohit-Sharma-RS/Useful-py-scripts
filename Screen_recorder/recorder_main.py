import cv2
import numpy as np
import pyautogui
import time
import threading
import keyboard

TIMEOUT = 3           # Seconds to wait after hotkey before recording starts
RECORD_SECONDS = 10000    # Duration to record max can remove
VIDEO_FILENAME = "screen_record.avi"
FRAME_RATE = 25.0      # Frames per second
SCREEN_SIZE = pyautogui.size()  # Screen resolution

recording = False 

def take_screenshot():
    # Function to take a screenshot and save it with a timestamped filename
    ts = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{ts}.png"
    img = pyautogui.screenshot()
    img.save(filename)
    print(f"Screenshot saved as {filename}")

def record_screen():
    global recording
    print(f"Recording will start in {TIMEOUT} seconds...")
    time.sleep(TIMEOUT)
    recording = True
    print("Recording started...")

    # Set up the video writer with the appropriate codec
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(VIDEO_FILENAME, fourcc, FRAME_RATE, (SCREEN_SIZE.width, SCREEN_SIZE.height))

    start_time = time.time()
    while recording and (time.time() - start_time) < RECORD_SECONDS:
        # Capture screenshot
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Get current mouse position and draw a red 2 thickness circle to simulate a pointer
        x, y = pyautogui.position()
        cv2.circle(frame, (x, y), 10, (0, 0, 255), 2) 
        
        # Write frame to video file
        out.write(frame)
        # q to quit
        cv2.imshow("Recording (Press 'q' to quit early)", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    recording = False
    out.release()
    cv2.destroyAllWindows()
    print("Recording stopped and saved.")

def start_recording_hotkey():
    global recording
    if not recording:
        print("Hotkey detected: Starting screen recording...")
        rec_thread = threading.Thread(target=record_screen)
        rec_thread.start()
    else:
        print("Recording is already in progress!")

def stop_recording_hotkey():
    global recording
    if recording:
        print("Stopping recording...")
        recording = False
    else:
        print("No active recording to stop.")

def background_hotkeys():
    # Alt+S to start the recording and other shortcuts binded to functions
    keyboard.add_hotkey("alt+s", start_recording_hotkey)
    keyboard.add_hotkey("alt+q", stop_recording_hotkey)
    keyboard.add_hotkey("s+s", take_screenshot)
    print("Hotkey set: Press 'Alt+S' to start screen recording.")
    print("Hotkey set: Press 'Alt+Q' to stop recording.")
    print("Hotkey set: Press 'S+S' to take a screenshot.")
    print("Press 'esc' to exit the hotkey listener.")
    keyboard.wait("esc")
    print("Exiting hotkey listener.")

if __name__ == "__main__":
    # main thread hotkey running
    background_hotkeys()
    print("Application terminated.")