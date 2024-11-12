import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        if isinstance(results, list):
            for result in results:
                emotion = result['dominant_emotion']
                x, y, w, h = result['region']['x'], result['region']['y'], result['region']['w'], result['region']['h']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, f"Emotion: {emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            emotion = results['dominant_emotion']
            x, y, w, h = results['region']['x'], results['region']['y'], results['region']['w'], results['region']['h']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"Emotion: {emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    except Exception as e:
        print("Face not detected or error in emotion detection:", e)
    
    cv2.imshow('Emotion Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
