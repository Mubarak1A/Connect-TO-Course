from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Course:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.now()
