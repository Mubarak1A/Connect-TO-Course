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

def add_user_details(username, password, email, is_admin=False):
    """Add user details to the database — password is stored hashed"""
    session = Session()
    try:
        # If this is the very first user in the database, promote to admin automatically
        user_count = session.query(User).count()
        if user_count == 0:
            is_admin = True

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email, is_admin=is_admin)
        session.add(new_user)
        session.commit()
        return new_user
    finally:
        Session.remove()

def get_course(course_id):
    """Retrieve single course by ID"""
    session = Session()
    try:
        return session.query(Course).get(int(course_id))
    except (ValueError, TypeError):
        return None
    finally:
        Session.remove()

def add_course(title, url, instructor):
    """Admin function: Create a new course"""
    session = Session()
    try:
        new_course = Course(title=title.strip(), url=url.strip(), instructor=instructor.strip())
        session.add(new_course)
        session.commit()
        return new_course
    finally:
        Session.remove()

def update_course(course_id, title, url, instructor):
    """Admin function: Update an existing course"""
    session = Session()
    try:
        course = session.query(Course).get(int(course_id))
        if course:
            course.title = title.strip()
            course.url = url.strip()
            course.instructor = instructor.strip()
            session.commit()
            return course
        return None
    finally:
        Session.remove()

def delete_course(course_id):
    """Admin function: Delete a course by ID"""
    session = Session()
    try:
        course = session.query(Course).get(int(course_id))
        if course:
            session.delete(course)
            session.commit()
            return True
        return False
    finally:
        Session.remove()

def get_system_stats():
    """Admin function: Get aggregate counts for users, courses, bookmarks"""
    session = Session()
    try:
        total_users = session.query(User).count()
        total_courses = session.query(Course).count()
        users = session.query(User).all()
        total_bookmarks = sum(len(u.get_bookmark()) for u in users)
        return {
            "total_users": total_users,
            "total_courses": total_courses,
            "total_bookmarks": total_bookmarks
        }
    finally:
        Session.remove()

def set_user_admin(username, is_admin=True):
    """Promote or demote user admin status"""
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            user.is_admin = is_admin
            session.commit()
            return True
        return False
    finally:
        Session.remove()
