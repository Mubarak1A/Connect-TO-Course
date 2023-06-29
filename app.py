from flask import Flask, render_template, request, redirect, url_for, session
import os
from sqlalchemy import create_engine, text, exc
import database
  
app = Flask(__name__)

email = "adesinamubarak123@gmail.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def check_login():
    username = request.form['username']
    passwd = request.form['password']
    
    with database.engine.connect() as conn:
        query1 = text("SELECT username, passwd FROM users WHERE username = :username AND passwd = :passwd")
        result = conn.execute(query1, {"username": username, "passwd": passwd})
        
    data = result.fetchall()
    
    if len(data) == 1:
        return render_template('User_page.html')
    
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        email = request.form['email']
        
        try:
            with database.engine.connect() as conn:
                query1 = text("SELECT username, passwd FROM users WHERE username = :username AND passwd = :passwd")
                result = conn.execute(query1, {"username": username, "passwd": passwd})

            data = result.fetchall()
            
            if len(data) == 0:
                query2 = text("INSERT INTO users (username, passwd, email) VALUES (:username, :passwd, :email)")
                result = conn.execute(query2, {"username": username, "passwd": passwd, "email": email})
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
        
        except exc.OperationalError as e:
            # Reestablish the connection and retry the query
            database.engine.dispose()
            database.engine.connect()
            return redirect(url_for('index'))

    return render_template('index.html')


    

if __name__ == '__main__':
    app.run(debug=True)
