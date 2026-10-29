#!/usr/bin/python3
"""
Seed script — populates the courses table with sample Udemy-style course data.
Run once after the database is set up:

    python seed.py

Requires DATABASE_URL (or individual DB_* env vars) to be set.
"""

from models import Course, engine, Base
from sqlalchemy.orm import sessionmaker

SAMPLE_COURSES = [
    {"title": "Complete Python Bootcamp: From Zero to Hero in Python", "url": "https://www.udemy.com/course/complete-python-bootcamp/", "instructor": "Jose Portilla"},
    {"title": "The Web Developer Bootcamp 2024", "url": "https://www.udemy.com/course/the-web-developer-bootcamp/", "instructor": "Colt Steele"},
    {"title": "100 Days of Code: The Complete Python Pro Bootcamp", "url": "https://www.udemy.com/course/100-days-of-code/", "instructor": "Angela Yu"},
    {"title": "JavaScript: Understanding the Weird Parts", "url": "https://www.udemy.com/course/understand-javascript/", "instructor": "Anthony Alicea"},
    {"title": "The Complete JavaScript Course 2024: From Zero to Expert!", "url": "https://www.udemy.com/course/the-complete-javascript-course/", "instructor": "Jonas Schmedtmann"},
    {"title": "React - The Complete Guide 2024 (incl. React Router & Redux)", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "instructor": "Maximilian Schwarzmuller"},
    {"title": "Django 4 and Python Full-Stack Developer Masterclass", "url": "https://www.udemy.com/course/django-and-python-full-stack-developer-masterclass/", "instructor": "Jose Portilla"},
    {"title": "Machine Learning A-Z: AI, Python & R + ChatGPT Prize 2024", "url": "https://www.udemy.com/course/machinelearning/", "instructor": "Kirill Eremenko"},
    {"title": "The Complete SQL Bootcamp: Go from Zero to Hero", "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/", "instructor": "Jose Portilla"},
    {"title": "AWS Certified Solutions Architect - Associate 2024", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate/", "instructor": "Stephane Maarek"},
    {"title": "Docker and Kubernetes: The Complete Guide", "url": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/", "instructor": "Stephen Grider"},
    {"title": "Node.js, Express, MongoDB & More: The Complete Bootcamp 2024", "url": "https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/", "instructor": "Jonas Schmedtmann"},
    {"title": "The Complete 2024 Web Development Bootcamp", "url": "https://www.udemy.com/course/the-complete-web-development-bootcamp/", "instructor": "Angela Yu"},
    {"title": "iOS & Swift - The Complete iOS App Development Bootcamp", "url": "https://www.udemy.com/course/ios-13-app-development-bootcamp/", "instructor": "Angela Yu"},
    {"title": "Flutter & Dart - The Complete Guide [2024 Edition]", "url": "https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/", "instructor": "Maximilian Schwarzmuller"},
    {"title": "Data Science and Machine Learning Bootcamp with R", "url": "https://www.udemy.com/course/data-science-and-machine-learning-bootcamp-with-r/", "instructor": "Jose Portilla"},
    {"title": "The Complete Digital Marketing Course - 12 Courses in 1", "url": "https://www.udemy.com/course/learn-digital-marketing-course/", "instructor": "Rob Percival"},
    {"title": "Automate the Boring Stuff with Python Programming", "url": "https://www.udemy.com/course/automate/", "instructor": "Al Sweigart"},
    {"title": "Master the Coding Interview: Data Structures + Algorithms", "url": "https://www.udemy.com/course/master-the-coding-interview-data-structures-algorithms/", "instructor": "Andrei Neagoie"},
    {"title": "Deep Learning A-Z 2024: Neural Networks, AI & ChatGPT Prize", "url": "https://www.udemy.com/course/deeplearning/", "instructor": "Kirill Eremenko"},
    {"title": "The Git & Github Bootcamp", "url": "https://www.udemy.com/course/git-and-github-bootcamp/", "instructor": "Colt Steele"},
    {"title": "Linux Command Line Basics", "url": "https://www.udemy.com/course/linux-command-line-volume1/", "instructor": "Jason Cannon"},
    {"title": "TypeScript: The Complete Developer's Guide", "url": "https://www.udemy.com/course/typescript-the-complete-developers-guide/", "instructor": "Stephen Grider"},
    {"title": "The Complete Cyber Security Course: Hackers Exposed!", "url": "https://www.udemy.com/course/the-complete-internet-security-privacy-course-volume-1/", "instructor": "Nathan House"},
    {"title": "Ethereum and Solidity: The Complete Developer's Guide", "url": "https://www.udemy.com/course/ethereum-and-solidity-the-complete-developers-guide/", "instructor": "Stephen Grider"},
    {"title": "GraphQL with React: The Complete Developers Guide", "url": "https://www.udemy.com/course/graphql-with-react-course/", "instructor": "Stephen Grider"},
    {"title": "Vue - The Complete Guide (incl. Router & Composition API)", "url": "https://www.udemy.com/course/vuejs-2-the-complete-guide/", "instructor": "Maximilian Schwarzmuller"},
    {"title": "PostgreSQL: The Complete Developer's Guide", "url": "https://www.udemy.com/course/sql-and-postgresql/", "instructor": "Stephen Grider"},
    {"title": "Kotlin for Android: Beginner to Advanced", "url": "https://www.udemy.com/course/kotlinmasterclass/", "instructor": "Catalin Stefan"},
    {"title": "The Complete Foundation Stock Trading Course", "url": "https://www.udemy.com/course/complete-foundation-stock-trading-course/", "instructor": "Mohsen Hassan"},
]


def seed():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    existing = session.query(Course).count()
    if existing > 0:
        print(f"Database already has {existing} courses. Skipping seed.")
        session.close()
        return

    for course_data in SAMPLE_COURSES:
        course = Course(
            title=course_data["title"],
            url=course_data["url"],
            instructor=course_data["instructor"]
        )
        session.add(course)

    session.commit()
    session.close()
    print(f"Successfully seeded {len(SAMPLE_COURSES)} courses!")


if __name__ == '__main__':
    seed()
