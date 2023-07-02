from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import database
import functionalties
import creds
from datetime import timedelta
import fetch_api_db

app = Flask (__name__)
app.secret_key = creds.app_key
app.permanent_session_lifetime = timedelta(minutes=5)

courses_list = fetch_api_db.assemble_data()
titles = fetch_api_db.get_titles()
courses_dict = {course['title']: course for course in courses_list}
saved_courses = []


courses = database.load_courses()
users = database.load_users()

@app.route("/")
def index():
    random_courses = functionalties.generate_courses(courses)
    return render_template("index.html", courses=random_courses)

@app.route("/user_page", methods=['GET', 'POST'])
def login():
    random_courses = functionalties.generate_courses(courses)
    
    if request.method == 'POST':
        session.permanent = True
        
        if 'signupbtn' in request.form:
            session['username'] = request.form['username']
            username = session['username']
            password = request.form['password']
            email = request.form['email']
            
            # Create a new user in the database
            database.add_user_details(username, password, email)
            
            flash("Signup Successful!")
            flash("You can proceed to Login.")
            return redirect(url_for('index', courses=random_courses))
        
        elif 'loginbtn' in request.form:
            session['username'] = request.form['username']
            username = session['username']
            password = request.form['password']
            
            # Validate credentials and perform login logic using the database
            if database.check_user_login(username, password):
                flash('Login Successful!')
                return redirect(url_for('user_page', courses=random_courses))
            else:
                flash("Invalid Login Details!")
                return redirect(url_for('index', courses=random_courses))

    
    else:
        if 'user_page' in session:
            flash("Already Logged In!")
            return redirect(url_for('user_page', courses=random_courses))
    
    return render_template("index.html", courses=random_courses)


@app.route('/search' , methods=['GET'])
def search():
    query = request.args.get('query', '')
    search_results = []

    search_titles = functionalties.search_courses(titles, query)
    courses = [courses_dict[title] for title in search_titles if title in courses_dict.keys()]
    for course in courses:
        search_results.append(course)

    return jsonify(results=search_results)


if __name__ == "__main__":
    app.run(debug=True)
