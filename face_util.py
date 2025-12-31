import cv2
import face_recognition
import numpy as np

def capture_face_encoding():
    cam = cv2.VideoCapture(0)
    encodings = []

    print("Look at camera. Press Q to capture.")

    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        faces = face_recognition.face_encodings(rgb, locations)

        if faces:
            encodings.append(faces[0])

        cv2.imshow("Capture Face", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

    if not encodings:
        return None

    return np.mean(encodings, axis=0)
