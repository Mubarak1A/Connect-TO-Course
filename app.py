from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import creds

app = Flask(__name__)
app.secret_key = '123'

db_username = creds.username
db_password = creds.passwd
db_host = creds.db_host
db_name = creds.database

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}?ssl_ca=/etc/ssl/cert.pem'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    instructor = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Course {self.title}>'


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signupbtn' in request.form:
            session['username'] = request.form['username']
            password = request.form['password']

            # Create a new user in the database
            user = User(username=session['username'], password=password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('userpage'))
        elif 'loginbtn' in request.form:
            session['username'] = request.form['username']
            password = request.form['password']

            # Validate credentials and perform login logic using the database
            user = User.query.filter_by(username=session['username'], password=password).first()
            if user:
                return redirect(url_for('userpage'))

    # Retrieve random courses and saved courses from the database
    r_results = Course.query.all()
    s_results = Course.query.all()

    return render_template('index.html', r_courses=r_results, s_courses=s_results)


@app.route("/user", methods=['GET', 'POST'])
def userpage():
    if 'username' in session:
        username = session['username']
        r_results = Course.query.all()
        return render_template('User_page.html', username=username, r_courses=r_results)
    else:
        return redirect(url_for('index'))


@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    search_results = Course.query.filter(Course.title.ilike(f'%{query}%')).all()

    return jsonify(results=[{
        'title': course.title,
        'instructor': course.instructor,
        'url': course.url,
        'course_id': course.course_id
    } for course in search_results])


if __name__ == '__main__':
    app.run(debug=True)
