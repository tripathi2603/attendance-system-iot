import os

if not os.path.exists("database.db"):
    open("database.db", "w").close()

from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/mark', methods=['POST'])
def mark():
    name = request.form['name']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # 🔥 check duplicate
    c.execute("SELECT * FROM attendance WHERE name=? AND time LIKE ?", (name, today+"%"))
    existing = c.fetchone()

    if existing:
        return "Attendance already marked today!"

    c.execute("INSERT INTO attendance (name, time) VALUES (?, ?)", (name, time))
    conn.commit()
    conn.close()

    return "Attendance Marked!"

# 🔥 Fingerprint with duplicate check
@app.route('/fingerprint')
def fingerprint():
    name = "User1"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM attendance WHERE name=? AND time LIKE ?", (name, today+"%"))
    existing = c.fetchone()
from flask import send_file
import csv

@app.route('/download')
def download():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    data = c.fetchall()
    conn.close()

    with open('attendance.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name', 'Time'])
        writer.writerows(data)

    return send_file('attendance.csv', as_attachment=True)

    if existing:
        return "Fingerprint already used today!"

    c.execute("INSERT INTO attendance (name, time) VALUES (?, ?)", (name, time))
    conn.commit()
    conn.close()

    return "Fingerprint Attendance Marked!"

app.run(debug=True)