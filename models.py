from datetime import datetime
import json
import os
from sqlalchemy import Column, Integer, String, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=True)
    bookmark = Column(Text, default="[]")
    is_admin = Column(Boolean, default=False)
    
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

# Db Connection — all credentials from environment variables
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')

# Support full DATABASE_URL as well (Neon / Render provide this directly)
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Neon and Render provide postgresql:// URLs; SQLAlchemy needs postgresql+psycopg2://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    elif database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    engine = create_engine(
        database_url,
        connect_args={"sslmode": "require"}
    )
else:
    engine = create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}/{db_name}",
        connect_args={"sslmode": "require"}
    )

Base.metadata.create_all(engine)
