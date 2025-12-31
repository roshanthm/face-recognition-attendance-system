import cv2
import face_recognition
import numpy as np

def capture_face_encoding():
    cap = cv2.VideoCapture(0)
    encodings = []

    print("Look at camera. Press Q to finish.")

    while True:
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb)
        faces = face_recognition.face_encodings(rgb, locations)

        for f in faces:
            encodings.append(f)

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(encodings) < 5:
        return None

    return np.mean(encodings, axis=0)
