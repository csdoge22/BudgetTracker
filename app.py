import os
from flask import Flask, redirect, render_template, request, url_for
# For the database, I am using SQLite as opposed to MySQL or PostgreSQL as this is a relatively small app
import sqlite3

app = Flask(__name__)

dbconn = sqlite3.connect("databases/thedb.db")
logdbcur = dbconn.cursor()

loginCommand = """
CREATE TABLE IF NOT EXISTS login(
    username TEXT PRIMARY KEY,
    password TEXT
)
"""
logdbcur.execute(loginCommand)

"""
Database Utilities:
"""

# checks to see if a user is already logged in
def __userExistsInLoginDB(name : str) -> bool:
    logdbcur.execute("SELECT username FROM login WHERE username=?", (name,))
    result = logdbcur.fetchall()
    return len(result)>0

# adds a user to the database
def __addUserToLoginDB(name : str, password : str):
    if(not __userExistsInLoginDB(name)):
        logdbcur.execute("INSERT INTO login (username, password) VALUES (?,?)",(name,password,))
    
# retrieve all records from the login database
def __fetchLoginDB():
    logdbcur.execute("SELECT * FROM login")
    result = logdbcur.fetchall()
    return result;

# delete user from login database if they choose not to have an account anymore
def __deleteUserFromLoginDB(name : str):
    logdbcur.execute("DELETE FROM login WHERE username=?", (name,))

"""
Page Routes:
/ is the signup page
/login is the login page
/home-page is the user interface to add, view, update, and delete contacts
/contacts is a dedicated contacts page that after clicking the button view contacts will show a table
"""

@app.route('/')
def signup():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/home-page', methods=['GET','POST'])
def home():
    user = request.form.get('user')
    password = request.form.get('pass')
    if(request.method=='POST'):
        __addUserToLoginDB(user,password)
        return render_template("user.html", user=user)
    else:
        return redirect(url_for('signup'))
    
if(__name__=='__main__'):
    app.run(debug=True)
    
logdbcur.close()
dbconn.close()