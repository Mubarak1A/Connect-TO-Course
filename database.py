import json
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Course, engine

# Scoped session — thread-safe, one session per request context
Session = scoped_session(sessionmaker(bind=engine))


def load_courses():
    """Load all courses from the database"""
    session = Session()
    try:
        return session.query(Course).all()
    finally:
        Session.remove()

def load_users():
    """Load all users from the database"""
    session = Session()
    try:
        return session.query(User).all()
    finally:
        Session.remove()

def get_user(user_id):
    """Retrieve user information from the database by user ID"""
    session = Session()
    try:
        return session.query(User).get(user_id)
    finally:
        Session.remove()

def load_bookmark(user_id):
    """Load all user saved courses_id"""
    session = Session()
    try:
        user = session.query(User).get(user_id)
        if user:
            return user.get_bookmark()
        else:
            return []
    finally:
        Session.remove()

def load_bookmark_list(user_id):
    """Load the saved courses with complete information"""
    session = Session()
    try:
        bookmark_ids = load_bookmark(user_id)
        bookmarked_courses = session.query(Course).filter(Course.id.in_(bookmark_ids)).all()

        bookmarked_courses_data = [
            {
                'id': course.id,
                'title': course.title,
                'url': course.url,
                'instructor': course.instructor
            }
            for course in bookmarked_courses
        ]
        return bookmarked_courses_data
    finally:
        Session.remove()

def save_course(user_id, course_id):
    """Save/bookmark course by storing the id"""
    session = Session()
    try:
        user = session.query(User).get(user_id)
        if not user:
            return False
        bookmark_ids = [int(i) for i in user.get_bookmark()]
        try:
            cid = int(course_id)
        except (ValueError, TypeError):
            return False

        if cid not in bookmark_ids:
            bookmark_ids.append(cid)
            user.set_bookmark(bookmark_ids)
            session.commit()
        return True
    finally:
        Session.remove()

def delete_bookmark(user_id, course_id):
    """Delete a particular course id from bookmark"""
    session = Session()
    try:
        user = session.query(User).get(user_id)
        if not user:
            return False
        bookmark_ids = [int(i) for i in user.get_bookmark()]
        try:
            cid = int(course_id)
        except (ValueError, TypeError):
            return False

        if cid in bookmark_ids:
            bookmark_ids.remove(cid)
            user.set_bookmark(bookmark_ids)
            session.commit()
        return True
    finally:
        Session.remove()

def get_user_by_username(username):
    """Check if a username already exists in the database"""
    session = Session()
    try:
        return session.query(User).filter_by(username=username).first()
    finally:
        Session.remove()

def get_user_by_email(email):
    """Check if an email already exists in the database"""
    session = Session()
    try:
        return session.query(User).filter_by(email=email).first()
    finally:
        Session.remove()

def check_user_login(username, passwd):
    """Check user credentials — verifies against hashed password"""
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, passwd):
            return user
        return None
    finally:
        Session.remove()

def add_user_details(username, password, email):
    """Add user details to the database — password is stored hashed"""
    session = Session()
    try:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        session.add(new_user)
        session.commit()
        print("User Details Added Successfully!")
    finally:
        Session.remove()
