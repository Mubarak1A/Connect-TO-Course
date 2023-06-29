from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from models import User, Course
#from database import courses
  
app = Flask(__name__)

app.secret_key = '123'
username = 'Elizabeth'


# Sample user for login demonstration
sample_user = User(username='Elizabeth', password='12345')
# Sample courses from database to test frontend. Remove it
courses = [
        {'title': 'Beginers guide to python', 'instructor': 'Elizabeth .A', 'url': 'www.udemy/course1', 'course_id': '123'},
        {'title': 'Basic guide to C', 'instructor': 'Elizabeth .A', 'url': 'www.udemy/course2', 'course_id': '456'},
        {'title': 'Beginers guide to flask', 'instructor': 'Mubarak. O', 'url': 'www.udemy/course3', 'course_id': '789'},
        {'title': 'Advance python', 'instructor': 'Olatunji .A', 'url': 'www.udemy/course4', 'course_id': '234'},
        {'title': 'Python for all', 'instructor': 'Elizabeth .O', 'url': 'www.udemy/course5', 'course_id': '128'},
        {'title': 'Python 2023', 'instructor': 'Elizabeth .A', 'url': 'www.udemy/course6', 'course_id': '127'}
    ]



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signupbtn' in request.form:
            session['username'] = request.form['username']
            password = request.form['password']

            # Please validate input and create user in the database.

            return redirect(url_for('userpage'))
        elif 'loginbtn' in request.form:
            session['username'] = request.form['username']
            password = request.form['password']

            # Please validate credentials and perform login logic.

            if username == sample_user.username and password == sample_user.password:
                return redirect(url_for('userpage'))
    
    #For testing.
    #Please be r_courses be the random courses, s_courses for saved courses.
    r_results = []
    for item in courses:
        r_results.append(item)                                              

    return render_template('index.html', r_courses=r_results, s_courses=r_results)


@app.route("/user", methods=['GET', 'POST'])
def userpage():
    if 'username' in session:
        username = session['username']
        r_results = []
        for item in courses:
            r_results.append(item)
        return render_template('User_page.html', username=username, r_courses=r_results)
    else:
        return redirect(url_for('index'))

@app.route("/logout", methods=['POST'])
def logout():
    # Clear the user session or perform any other necessary cleanup
    # ...
    session.clear()
    return redirect(url_for('home'))


@app.route('/search' , methods=['GET'])
def search():
    query = request.args.get('query', '')

    search_results = []
    for item in courses:
        if query.lower() in item['title'].lower():
            search_results.append(item)

    return jsonify(results=search_results)


if __name__ == '__main__':
    app.run(debug=True)
