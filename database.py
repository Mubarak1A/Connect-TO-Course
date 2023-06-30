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
    courses = []
    with engine.connect() as conn:
        results = conn.execute(text("SELECT * FROM courses"))

        for course in results.fetchall():
            courses.append(course)
    return courses

#print(load_courses())





