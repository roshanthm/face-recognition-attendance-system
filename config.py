import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "attendance.db")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "known_faces")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
