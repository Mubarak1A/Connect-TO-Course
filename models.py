from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
import creds

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bookmark = Column(Text, default="[]")
    
    def get_bookmark(self):
        return json.loads(self.bookmark)
    
    def set_bookmark(self, bookmark):
        self.bookmark = json.dumps(bookmark)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    instructor = Column(String, nullable=False)

    def __str__(self):
        return f"course_id: {self.id}, title: {self.title}, url: {self.url}, instructor: {self.instructor}"

# Db Connection
db_username = creds.username
db_password = creds.passwd
db_host = creds.db_host
db_name = creds.database

engine = create_engine(
    f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}",
    connect_args={"sslmode": "require"}
)
Base.metadata.create_all(engine)
