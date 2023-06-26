from flask import Flask, render_template, request, redirect, url_for, session, g
import os
from models import User, Course
  
app = Flask(__name__)

app.secret_key = '123'
username = 'Elizabeth'

# Sample user for login demonstration
sample_user = User(username='Elizabeth', password='12345')

#@app.route('/index', methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signupbtn' in request.form:
            session['username'] = request.form['username']
            password = request.form['password']

            # @Mubarak: Please validate input and create user in the database.

            return redirect(url_for('userpage'))
        elif 'loginbtn' in request.form:
            session['username'] = request.form['username']
            password = request.form['password']

            # @Mubarak: Please validate credentials and perform login logic.

            if username == sample_user.username and password == sample_user.password:
                return redirect(url_for('userpage'))
    return render_template('index.html')
    

@app.route("/user", methods=['GET', 'POST'])
def userpage():
    if 'username' in session:
        username = session['username']
        return render_template('User_page.html', username=username)
    else:
        return redirect(url_for('index'))

@app.route("/logout", methods=['POST'])
def logout():
    # Clear the user session or perform any other necessary cleanup
    # ...
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
