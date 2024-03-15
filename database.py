#!/usr/bin/python3
"""Database module to connect to the cloud database"""

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

def load_bookmark(user_id):
    """Load all user saved courses_id"""
    user = session.query(User).get(user_id)
    if user:
        bookmark_ids = [int(id) for id in user.bookmark.split(" ") if id]
    else:
        bookmark_ids = []
    return bookmark_ids

def load_bookmark_list(user_id):
    """Load the saved courses"""
    bookmark_ids = load_bookmark(user_id)
    all_courses = load_courses()

    filtered_courses_list = [
        course for course in all_courses if course.id in bookmark_ids
    ]
    filtered_courses = [
        {
            'id': course.id,
            'title': course.title,
            'url': course.url,
            'instructor': course.instructor
        }
        for course in filtered_courses_list
    ]

    return filtered_courses

def save_course(user_id, course_id):
    """Save/bookmark course by storing the id"""
    user = session.query(User).get(user_id)
    if user:
        bookmark_ids = [int(id) for id in user.bookmark.split(" ") if id]
    else:
        bookmark_ids = []

    if course_id not in bookmark_ids:
        bookmark_ids.append(course_id)

    user.bookmark = " ".join(str(id) for id in bookmark_ids)
    session.commit()

def delete_bookmark(user_id, course_id):
    """Delete a particular course id from bookmark"""
    user = session.query(User).get(user_id)
    if user:
        bookmark_ids = [int(id) for id in user.bookmark.split(" ") if id]
    else:
        bookmark_ids = []

    if course_id in bookmark_ids:
        bookmark_ids.remove(course_id)

    user.bookmark = " ".join(str(id) for id in bookmark_ids)
    session.commit()

def check_user_login(username, passwd):
    """Check if user details in the database"""
    user = session.query(User).filter_by(username=username, password=passwd).first()
    return user

def add_user_details(username, password, email):
    """Add user details to the database"""
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    print("User Details Added Successfully!")
