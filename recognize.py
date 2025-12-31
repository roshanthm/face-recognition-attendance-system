def mark_attendance():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT emp_id, embedding FROM embeddings")
    data = cur.fetchall()

    known_encodings = [np.frombuffer(e, dtype=np.float64) for _, e in data]
    emp_ids = [i for i, _ in data]

    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for enc in encodings:
            matches = face_recognition.compare_faces(known_encodings, enc, tolerance=0.45)
            if True in matches:
                idx = matches.index(True)
                emp_id = emp_ids[idx]

                now = datetime.now()
                cur.execute(
                    "INSERT INTO attendance VALUES (?, ?, ?)",
                    (emp_id, now.date().isoformat(), now.time().isoformat())
                )
                conn.commit()
                cam.release()
                cv2.destroyAllWindows()
                return emp_id

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
    raise Exception("No face recognized")
