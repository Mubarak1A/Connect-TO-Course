from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g, flash
import os
from models import User, Course
import database
import functionalties


app = Flask(__name__)

app.secret_key = '123'
username = 'Elizabeth'

courses = database.load_courses()
saved_courses = []
random_courses = functionalties.generate_courses(courses)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signupbtn' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # Create a new user in the database
            database.add_user_details(username, password, email)

            flash("Signup Successful!")
            flash("You can proceed to Login.")
            return redirect(url_for('index'))

        elif 'loginbtn' in request.form:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            username = request.form['username']
            password = request.form['password']

            # Validate credentials and perform login logic.
            if database.check_user_login(username, password):
                flash('Login Successful!')
                user_id=database.check_user_login(username, password)
                return redirect(url_for('userpage'))
            else:
                flash("Invalid Login Details!")
                return redirect(url_for('index'))

    return render_template('index.html', random_courses=random_courses)


@app.route("/user", methods=['GET', 'POST'])
def userpage():
    if 'username' in session and 'password' in session:
        username = session['username']
        password = session['password']
        user_id = database.check_user_login(username, password)
        saved_courses=database.load_bookmark_list(user_id)

        return render_template('User_page.html', username=username, random_courses=random_courses, saved_courses=saved_courses, user_id=user_id)
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
    
    #app.logger.info("Route /save triggered")
    #update the bookmark and return courses to the user page.
    #saved_courses=database.load_bookmark_list(user_id)
    #return jsonify(results=saved_courses)

    return redirect(url_for('userpage'))


@app.route('/delete', methods=['POST'])
def delete():
    #Retrieve the course url and username.
    data = request.get_json(force=True)
    course_id = data.get('id')
    user_id = data.get('user_id')
    
    #delete course
    database.delete_bookmark(user_id, course_id)
    app.logger.info("Route /delete triggered")
    return redirect(url_for('userpage'))


@app.route('/landing_page', methods=['GET'])
def landingPage():
    return render_template('landing_page.html')


if __name__ == '__main__':
    app.run(debug=True)
