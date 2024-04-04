import json
from sqlalchemy.orm import sessionmaker
from models import User, Course, engine

# Create a Session class to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

def load_courses():
    """Load all courses from the database"""
    return session.query(Course).all()

def load_users():
    """Load all users from the database"""
    return session.query(User).all()

def get_user(user_id):
    """Retrieve user information from the database by user ID"""
    return session.query(User).get(user_id)

def load_bookmark(user_id):
    """Load all user saved courses_id"""
    user = session.query(User).get(user_id)
    if user:
        return user.get_bookmark()  # Use get_bookmark method
    else:
        return []

def load_bookmark_list(user_id):
    """Load the saved courses with complete information"""
    bookmark_ids = load_bookmark(user_id)
    bookmarked_courses = session.query(Course).filter(Course.id.in_(bookmark_ids)).all()

    # Convert bookmarked courses to a list of dictionaries
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

def save_course(user_id, course_id):
    """Save/bookmark course by storing the id"""
    user = session.query(User).get(user_id)
    if user:
        bookmark_ids = user.get_bookmark()  # Use get_bookmark method
    else:
        bookmark_ids = []

    if course_id not in bookmark_ids:
        bookmark_ids.append(course_id)

    user.set_bookmark(bookmark_ids)  # Use set_bookmark method
    session.commit()

def delete_bookmark(user_id, course_id):
    """Delete a particular course id from bookmark"""
    user = session.query(User).get(user_id)
    if user:
        bookmark_ids = user.get_bookmark()  # Use get_bookmark method
    else:
        bookmark_ids = []

    if course_id in bookmark_ids:
        bookmark_ids.remove(course_id)

    user.set_bookmark(bookmark_ids)  # Use set_bookmark method
    session.commit()

def check_user_login(username, passwd):
    """Check if user details in the database"""
    return session.query(User).filter_by(username=username, password=passwd).first()

def add_user_details(username, password, email):
    """Add user details to the database"""
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    print("User Details Added Successfully!")
