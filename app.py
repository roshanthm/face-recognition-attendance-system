from flask import Flask, request, jsonify, send_file
from datetime import datetime
import numpy as np
import face_recognition
import pandas as pd
import os

from database import init_db, get_db
from face_utils import capture_face_encoding

app = Flask(__name__)

# Initialize DB (creates tables if missing)
init_db()

# -------------------------------------------------
# HOME
# -------------------------------------------------
@app.route("/")
def home():
    return "Face Recognition Attendance Backend Running"

# -------------------------------------------------
# REGISTER STUDENT (FACE ENROLLMENT)
# -------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    roll_no = data.get("roll_no")
    name = data.get("name")

    if not roll_no or not name:
        return jsonify({"error": "roll_no and name required"}), 400

    encoding = capture_face_encoding()
    if encoding is None:
        return jsonify({"error": "No face detected"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO students (roll_no, name, encoding) VALUES (?, ?, ?)",
            (roll_no, name, encoding.tobytes())
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400

    conn.close()
    return jsonify({"message": "Student registered successfully"})

# -------------------------------------------------
# MARK ATTENDANCE
# -------------------------------------------------
@app.route("/attendance", methods=["POST"])
def mark_attendance():
    encoding = capture_face_encoding()
    if encoding is None:
        return jsonify({"error": "No face detected"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT roll_no, encoding FROM students")
    records = cur.fetchall()

    if not records:
        conn.close()
        return jsonify({"error": "No students registered"}), 400

    known_encodings = [np.frombuffer(r[1], dtype=np.float64) for r in records]
    roll_nos = [r[0] for r in records]

    matches = face_recognition.compare_faces(
        known_encodings, encoding, tolerance=0.45
    )

    if True not in matches:
        conn.close()
        return jsonify({"error": "Face not recognized"}), 404

    roll_no = roll_nos[matches.index(True)]
    now = datetime.now()

    # Prevent duplicate attendance for same day
    cur.execute(
        "SELECT 1 FROM attendance WHERE roll_no=? AND date=?",
        (roll_no, now.date().isoformat())
    )
    if cur.fetchone():
        conn.close()
        return jsonify({"message": f"Attendance already marked for {roll_no}"})

    cur.execute(
        "INSERT INTO attendance (roll_no, date, time) VALUES (?, ?, ?)",
        (roll_no, now.date().isoformat(), now.time().strftime("%H:%M:%S"))
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"Attendance marked for {roll_no}"})

# -------------------------------------------------
# ADMIN: VIEW STUDENTS
# -------------------------------------------------
@app.route("/admin/students")
def admin_students():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT roll_no, name FROM students")
    data = cur.fetchall()
    conn.close()
    return jsonify(data)

# -------------------------------------------------
# ADMIN: VIEW ATTENDANCE
# -------------------------------------------------
@app.route("/admin/attendance")
def admin_attendance():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT roll_no, date, time FROM attendance")
    data = cur.fetchall()
    conn.close()
    return jsonify(data)

# -------------------------------------------------
# ADMIN: EXPORT ATTENDANCE TO EXCEL
# -------------------------------------------------
@app.route("/admin/export")
def export_attendance():
    conn = get_db()
    df = pd.read_sql_query(
        "SELECT roll_no, date, time FROM attendance",
        conn
    )
    conn.close()

    os.makedirs("exports", exist_ok=True)
    file_path = "exports/attendance.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)

# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
