from flask import Flask, render_template, request, redirect, url_for, session, g
import os
from models import User, Course
  
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

# Sample user for login demonstration
sample_user = User(username='Elizabeth', password='12345')

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
