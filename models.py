from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    instructor = Column(String, nullable=False)

    def __str__(self):
        return f"course_id: {self.id}, title: {self.title}, url: {self.url}, instructor: {self.instructor}"

# Db Connection

engine = create_engine("postgresql://your_username:your_password@localhost/your_database")
Base.metadata.create_all(engine)
