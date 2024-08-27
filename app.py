from flask import Flask, flash, redirect, render_template, request, url_for, session
import sqlite3
import time
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

app = Flask(__name__)


# Initialize the SQLite database
def initdb():
    with sqlite3.connect("databases/thedb.db") as dbconn:
        dbconn.execute("""
        CREATE TABLE IF NOT EXISTS login(
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """)
        dbconn.commit()

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
