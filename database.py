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

def check_user_login(username, passwd):
    """check if user details in database"""
    users = load_users()

    for user in users:
        if user[1] == username and user[2] == passwd:
            return True
    else:
        return False


#print(load_courses())
#print(check_user_login("mub", "123"))




