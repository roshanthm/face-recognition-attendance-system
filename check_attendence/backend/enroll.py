import cv2
import face_recognition
import numpy as np
from database import connect

def enroll(emp_id, name):
    cam = cv2.VideoCapture(0)
    encodings = []

    print("Look at camera. Press Q to finish.")

    while True:
        ret, frame = cam.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        face_encs = face_recognition.face_encodings(rgb, faces)

        for enc in face_encs:
            encodings.append(enc)

        cv2.imshow("Enrollment", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    if len(encodings) < 5:
        print("Not enough data")
        return

    avg = np.mean(encodings, axis=0)

    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO employees VALUES (?,?)", (emp_id, name))
    cur.execute("INSERT INTO embeddings VALUES (?,?)", (emp_id, avg.tobytes()))
    conn.commit()
    conn.close()

    print("Enrollment successful")

if __name__ == "__main__":
    emp_id = input("Employee ID: ")
    name = input("Name: ")
    enroll(emp_id, name)
