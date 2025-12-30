import cv2, face_recognition, numpy as np
from datetime import datetime
from database import connect

def recognize():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT emp_id, embedding FROM embeddings")
    data = cur.fetchall()

    known = [np.frombuffer(e, dtype=np.float64) for _, e in data]
    ids = [i for i, _ in data]

    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, locs)

        for enc in encs:
            matches = face_recognition.compare_faces(known, enc, 0.45)
            if True in matches:
                idx = matches.index(True)
                emp_id = ids[idx]

                now = datetime.now()
                cur.execute(
                    "INSERT INTO attendance VALUES (?,?,?)",
                    (emp_id, now.date().isoformat(), now.time().isoformat())
                )
                conn.commit()
                print("Attendance marked:", emp_id)
                cam.release()
                cv2.destroyAllWindows()
                return

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize()
