from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def signup():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home-page', methods=['GET','POST'])
def home():
    user = request.form.get('user')
    if(request.method=='POST'):
        return render_template("user.html", user=user)
    else:
        return redirect(url_for('signup'))
    
if(__name__=='__main__'):
    app.run(debug=True)