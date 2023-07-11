from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g, flash
import os
from models import User, Course
import database
import fetch_api_db
import functionalties


app = Flask(__name__)

app.secret_key = '123'
username = 'Elizabeth'


courses = database.load_courses()
courses_list = fetch_api_db.assemble_data()
titles = fetch_api_db.get_titles()
courses_dict = {course['title']: course for course in courses_list}
saved_courses = []


@app.route("/", methods=['GET', 'POST'])
def index():
    random_courses = functionalties.generate_courses(courses)
    r_results = random_courses
    if request.method == 'POST':
        if 'signupbtn' in request.form:
            session['username'] = request.form['username']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # Please validate input and create user in the database.
            # Create a new user in the database
            database.add_user_details(username, password, email)

            flash("Signup Successful!")
            flash("You can proceed to Login.")
            return redirect(url_for('index', courses=random_courses))

            #return redirect(url_for('userpage'))
        elif 'loginbtn' in request.form:
            username = request.form['username']
            password = request.form['password']

            # Please validate credentials and perform login logic.
            if database.check_user_login(username, password):
                flash('Login Successful!')
                return redirect(url_for('userpage'))
            else:
                flash("Invalid Login Details!")
                return redirect(url_for('index'))

    return render_template('index.html', r_courses=r_results, s_courses=r_results)


@app.route("/user", methods=['GET', 'POST'])
def userpage():
    if 'username' in session:
        username = session['username']

        random_courses = functionalties.generate_courses(courses)
        r_results = random_courses

        return render_template('User_page.html', username=username, r_courses=r_results)
    else:
        return redirect(url_for('index'))


@app.route("/logout", methods=['POST'])
def logout():
    # Clear the user session or perform any other necessary cleanup
    session.clear()
    return redirect(url_for('index'))


@app.route('/search' , methods=['GET'])
def search():
    query = request.args.get('query', '')

    search_results = []
    search_titles = functionalties.search_courses(titles, query)
    courses = [courses_dict[title] for title in search_titles if title in courses_dict.keys()]
    for course in courses:
        search_results.append(course)

    return jsonify(results=search_results)


@app.route('/save' , methods=['GET'])
def save():
    if request.args.get('name'):
        query = request.args.get('name', '')
        #Save the course for the user

    #update the bookmark and return it to user page.
    return jsonify(results=saved_courses)


@app.route('/landing_page', methods=['GET'])
def landingPage():
    return render_template('landing_page.html')


if __name__ == '__main__':
    app.run(debug=True)
