from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_wtf.csrf import CSRFProtect
from functools import wraps
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from models import User, Course
import database
import functionalties
import seed


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback-secret-change-in-prod')

# CSRF protection — applies to all state-changing requests
csrf = CSRFProtect(app)

# Auto-seed the database with sample courses if it's empty
seed.seed()


@app.route("/", methods=['GET', 'POST'])
def index():
    courses = database.load_courses()
    random_courses = functionalties.generate_courses(courses)
    if request.method == 'POST':
        if 'signupbtn' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # Check for duplicate username or email
            if database.get_user_by_username(username):
                flash("Username already taken. Please choose another.", "failure")
                return redirect(url_for('index'))
            if database.get_user_by_email(email):
                flash("Email already registered. Please log in.", "failure")
                return redirect(url_for('index'))

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
                session['is_admin'] = bool(user.is_admin)
                flash('Login Successful!', 'login')
                if user.is_admin:
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('userpage'))
            else:
                flash("Invalid Login Details!", "failure")
                return redirect(url_for('index'))

    user = None
    saved_courses = []
    if 'user_id' in session:
        user = database.get_user(session['user_id'])
        if user:
            saved_courses = database.load_bookmark_list(user.id)

    return render_template(
        'index.html',
        random_courses=random_courses,
        saved_courses=saved_courses,
        username=user.username if user else None
    )



@app.route("/user", methods=['GET', 'POST'])
def userpage():
    courses = database.load_courses()
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


@app.route('/search', methods=['GET'])
def search():
    # Get the query to search for
    query = request.args.get('query', '')

    # Load courses from database
    courses = database.load_courses()

    # Search and return json
    search_titles = functionalties.search_courses(courses, query)
    return jsonify(results=search_titles)


@app.route('/save', methods=['POST'])
@csrf.exempt
def save():
    data = request.get_json(force=True) or {}
    course_id = data.get('id')
    user_id = data.get('user_id') or session.get('user_id')

    if not user_id:
        return jsonify(status="error", message="Authentication required"), 401

    if not course_id:
        return jsonify(status="error", message="Course ID is required"), 400

    success = database.save_course(user_id, course_id)
    if not success:
        return jsonify(status="error", message="Failed to save course"), 400

    bookmark_ids = database.load_bookmark(user_id)
    return jsonify(
        status="success",
        message="Course saved successfully",
        course_id=course_id,
        bookmark_count=len(bookmark_ids)
    )


@app.route("/delete", methods=['POST'])
@csrf.exempt
def delete():
    data = request.get_json(force=True) or {}
    course_id = data.get('id')
    user_id = data.get('user_id') or session.get('user_id')

    if not user_id:
        return jsonify(status="error", message="Authentication required"), 401

    if not course_id:
        return jsonify(status="error", message="Course ID is required"), 400

    success = database.delete_bookmark(user_id, course_id)
    if not success:
        return jsonify(status="error", message="Failed to delete bookmark"), 400

    bookmark_ids = database.load_bookmark(user_id)
    return jsonify(
        status="success",
        message="Bookmark removed successfully",
        course_id=course_id,
        bookmark_count=len(bookmark_ids)
    )


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash("Please log in as an administrator to access the admin panel.", "warning")
            return redirect(url_for('index'))
        user = database.get_user(user_id)
        if not user or not user.is_admin:
            flash("Access denied. Administrator privileges required.", "failure")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard — course management and analytics"""
    courses = database.load_courses()
    stats = database.get_system_stats()
    user = database.get_user(session['user_id'])
    return render_template(
        'admin.html',
        courses=courses,
        stats=stats,
        username=user.username
    )


@app.route('/admin/course/add', methods=['POST'])
@admin_required
def admin_add_course():
    """Admin endpoint: Add a new course"""
    title = request.form.get('title')
    url = request.form.get('url')
    instructor = request.form.get('instructor')

    if not title or not url or not instructor:
        flash("All fields (title, url, instructor) are required.", "failure")
        return redirect(url_for('admin_dashboard'))

    database.add_course(title, url, instructor)
    flash(f"Course '{title}' successfully added!", "signup")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/course/edit/<int:course_id>', methods=['POST'])
@admin_required
def admin_edit_course(course_id):
    """Admin endpoint: Update an existing course"""
    title = request.form.get('title')
    url = request.form.get('url')
    instructor = request.form.get('instructor')

    updated = database.update_course(course_id, title, url, instructor)
    if updated:
        flash(f"Course '{title}' updated successfully!", "login")
    else:
        flash("Course not found or update failed.", "failure")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/course/delete/<int:course_id>', methods=['POST'])
@admin_required
def admin_delete_course(course_id):
    """Admin endpoint: Delete a course"""
    success = database.delete_course(course_id)
    if success:
        flash("Course deleted successfully.", "warning")
    else:
        flash("Failed to delete course.", "failure")
    return redirect(url_for('admin_dashboard'))


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Render and uptime monitoring"""
    return jsonify(status="ok", service="connect-to-course"), 200


@app.route('/courses_api')
def list_courses():
    courses = database.load_courses()
    courses_list = [{
        "id": course.id,
        "title": course.title,
        "url": course.url,
        "instructor": course.instructor
    } for course in courses]

    return jsonify(courses_list)


@app.route('/landing_page', methods=['GET'])
def landingPage():
    return render_template('landing_page.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
