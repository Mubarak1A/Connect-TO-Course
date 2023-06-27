from flask import Flask, render_template, request, redirect, url_for, session
import os
from sqlalchemy import create_engine, text
import database
  
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def check_login():
    username = request.form['username']
    passwd = request.form['password']
    
    with database.engine.connect() as conn:
        query1 = text("SELECT username, passwd FROM users WHERE username = :username AND passwd = :passwd")
        result = conn.execute(query1, username=username, passwd=passwd)
        
    data = result.fetchall()
    
    if len(data) == 1:
        return render_template('User_page.html')
        
    

if __name__ == '__main__':
    app.run(debug=True)
