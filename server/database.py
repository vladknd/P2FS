from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the User and File classes using SQLAlchemy ORM
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    port_number = Column(Integer)

    files = relationship("File", back_populates="user")

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    file = Column(String)

    user = relationship("User", back_populates="files")

# Create an engine to connect to the database
engine = create_engine('sqlite:///database_test.db', echo=True)

# Create the tables
Base.metadata.create_all(engine)

# Create a Session class to interact with the database
Session = sessionmaker(bind=engine)

# Functions used to interact with the databases
def insert_user(username, port_number):
    session = Session()
    user = User(id=username, port_number=port_number)
    session.add(user)
    session.commit()
    session.close()

def insert_file(user_id, file):
    session = Session()
    file_obj = File(id=user_id, file=file)
    session.add(file_obj)
    session.commit()
    session.close()

def fetch_all_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

def fetch_user_port_number(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    port_number = user.port_number if user else None
    session.close()
    return port_number

def fetch_file_table(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    files = [file.file for file in user.files] if user else None
    session.close()
    return files
