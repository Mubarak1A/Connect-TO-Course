from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g, flash
import os
from models import User, Course
import database
import functionalties


app = Flask(__name__)

app.secret_key = '123'

courses = database.load_courses()
saved_courses = []


@app.route("/", methods=['GET', 'POST'])
def index():
    random_courses = functionalties.generate_courses(courses)
    if request.method == 'POST':
        if 'signupbtn' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # Create a new user in the database
            database.add_user_details(username, password, email)

            flash("Sign up Successful!", "signup")
            flash("You can proceed to Login.", "signup")
            return redirect(url_for('index'))

        elif 'loginbtn' in request.form:
            username = request.form['username']
            password = request.form['password']

            # Validate credentials and perform login logic.
            user = database.check_user_login(username, password)
            if user:
                session['user_id'] = user.id  # Store only user_id in session
                flash('Login Successful!', 'login')
                return redirect(url_for('userpage'))
            else:
                flash("Invalid Login Details!", "failure")
                return redirect(url_for('index'))

    return render_template('index.html', random_courses=random_courses)



@app.route("/user", methods=['GET', 'POST'])
def userpage():
    random_courses = functionalties.generate_courses(courses)
    if 'user_id' in session:
        user_id = session['user_id']
        user = database.get_user(user_id)  # Retrieve user information from database
        if user:
            saved_courses = database.load_bookmark_list(user_id)
            return render_template('User_page.html', username=user.username, random_courses=random_courses, saved_courses=saved_courses, user_id=user_id)
        else:
            flash("Please login to access this page!", "warning")
            return redirect(url_for('index'))  # Invalidate session if user not found
    else:
        return redirect(url_for('index'))

@app.route("/logout", methods=['POST'])
def logout():
    # Clear the user session
    session.clear()
    return redirect(url_for('index'))


@app.route('/search' , methods=['GET'])
def search():
    #Get the query to search for
    query = request.args.get('query', '')

    #Load courses from database
    courses = database.load_courses()

    #Search and return json
    search_titles = functionalties.search_courses(courses, query)
    return jsonify(results=search_titles)


@app.route('/save' , methods=['POST'])
def save():
    #Retrieve the course url and username.
    data = request.get_json(force=True)
    course_id = data.get('id')
    user_id = data.get('user_id')

    #Save the course id to the database
    database.save_course(user_id, course_id)

    #return jsonify(results=saved_courses)
    return redirect(url_for('userpage'))


@app.route("/delete", methods=['POST'])
def delete():
    #Retrieve the course url and username.
    data = request.get_json(force=True)
    course_id = data.get('id')
    user_id = data.get('user_id')
    
    #delete course
    #app.logger.info(f"Deleting bookmark for user_id: {user_id}, course_id: {course_id}")
    database.delete_bookmark(user_id, course_id)

    return redirect(url_for('userpage'))
            

@app.route('/courses_api')
def list_courses():
    courses_list = [dict(course._asdict()) for course in courses]

    return jsonify(courses_list)



@app.route('/landing_page', methods=['GET'])
def landingPage():
    return render_template('landing_page.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
