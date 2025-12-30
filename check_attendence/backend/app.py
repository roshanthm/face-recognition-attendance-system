from fastapi import FastAPI
from database import connect

app = FastAPI()

@app.get("/employees")
def employees():
    cur = connect().cursor()
    cur.execute("SELECT * FROM employees")
    return cur.fetchall()

@app.get("/attendance")
def attendance():
    cur = connect().cursor()
    cur.execute("SELECT * FROM attendance")
    return cur.fetchall()
