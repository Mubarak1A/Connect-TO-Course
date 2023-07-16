from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Course:
    def __init__(self, id, title, url, instructor):
        self.id = id
        self.title = title
        self.url = url
        self.instructor = instructor

    def __str__(self):
        return f"course_id: {self.id}, title: {self.title}, url: {self.url}, instructor: {self.instructor}"
