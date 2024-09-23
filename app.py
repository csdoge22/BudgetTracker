from flask import Flask, flash, redirect, render_template, request, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

app = Flask(__name__)
app.secret_key = "kmasdfj8au32ja3n1i"

# Initialize the SQLite database
def initdb():
    with sqlite3.connect("databases/thedb.sqlite") as dbconn:
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

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        user = request.form['username']
        password = generate_password_hash(request.form['password'])
    
        with sqlite3.connect("databases/thedb.sqlite") as dbconn:
            dbcur = dbconn.cursor()
        
        # Correctly pass user as a tuple
            dbcur.execute("SELECT password FROM login WHERE username=?", (user,))
            result = dbcur.fetchall()
        
            if not result:
                dbcur.execute("""
                INSERT INTO login (username, password)
                VALUES (?, ?)
                """, (user, password))
                dbconn.commit()
    
        dbcur.execute("SELECT username FROM login")
        usernameDB = dbcur.fetchall()
        print("DATABASE CONTENTS: ")
        print(usernameDB)

        return render_template("user.html", user=user, usernameDB=usernameDB, numElements=len(usernameDB))
    error = 'Sorry! But please login first'
    flash(error)
    return render_template("index.html", error=error)



if __name__ == '__main__':
    app.run(debug=True)
