#!/usr/bin/python3
"""Database module to connect to the cloud database"""

from sqlalchemy import create_engine, text
import creds

db_username = creds.username
db_password = creds.passwd
db_host = creds.db_host
db_name = creds.database

engine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(db_username, db_password, db_host, db_name),
                       connect_args = {
                           "ssl": {
                               "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })

def load_courses():
    """load all courses from database"""
    courses = []
    with engine.connect() as conn:
        results = conn.execute(text("SELECT * FROM courses"))

        for course in results.fetchall():
            courses.append(course)
    return courses

def load_users():
    """load users from database"""
    users = []
    with engine.connect() as conn:
        results = conn.execute(text("SELECT * FROM users"))

        for user in results.fetchall():
            users.append(user)
    return users


def load_bookmark(user_id):
    """load all user saved courses_id"""
    with engine.connect() as conn:
        results = conn.execute(text("SELECT bookmark FROM users WHERE id = {}".format(user_id)))
    bookmark_courses = results.fetchone()[0]
    if bookmark_courses:
        bookmark_ids = [int(id) for id in bookmark_courses.split(" ")]
    else:
        bookmark_ids = []
    
    return (bookmark_ids)


def load_bookmark_list(user_id):
    """load the saved courses"""
    bookmark_ids = load_bookmark(user_id)
    #load all courses
    all_courses = load_courses()

    filtered_courses_list = [
        course for course in all_courses if course.id in bookmark_ids
    ]
    filtered_courses = [
        {
            'id': course[0],
            'title': course[1],
            'url': course[2],
            'instructor': course[3]
        }
        for course in filtered_courses_list
    ]

    return (filtered_courses)

    


def save_course(user_id, course_id):
    """save/bookmark course by storing the id"""
    bookmark_list = load_bookmark(user_id)

    if course_id not in bookmark_list:
        bookmark_list.append(course_id)

    new_bookmark = " ".join(str(id) for id in bookmark_list)

    with engine.connect() as conn2:
        conn2.execute(text("UPDATE users SET bookmark = '{}' WHERE id = {}".format(new_bookmark, user_id)))

    return 0



def delete_bookmark(user_id, course_id):
    """Delete a particular course id from bookmark"""
    bookmark_list = load_bookmark(user_id)

    if course_id in bookmark_list:
        bookmark_list.remove(course_id)
    new_bookmark = " ".join(str(id) for id in bookmark_list)
    
    with engine.connect() as conn2:
        conn2.execute(text("UPDATE users SET bookmark = '{}' WHERE id = {}".format(new_bookmark, user_id)))

    return 0



def check_user_login(username, passwd):
    """check if user details in database"""
    users = load_users()

    for user in users:
        if user[1] == username and user[3] == passwd:
            return user[0]
    else:
        return False

def add_user_details(username, password, email):
    """add user details to database"""
    with engine.connect() as conn:
        query = text("INSERT INTO users (username, email, passwd) VALUES (:username, :email, :passwd)")
        result = conn.execute(query, {"username": username, "email": email, "passwd": password})
        print("User Details Added Successfully!")

