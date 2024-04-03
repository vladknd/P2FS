from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class RegisteredUser(Base):
    __tablename__ = 'registered_users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    ip_address = Column(String, nullable=False)
    udp_socket = Column(Integer, nullable=False)

# Setup SQLite database
engine = create_engine('sqlite:///registration.db')
Base.metadata.create_all(engine)

# Create a Session
Session = sessionmaker(bind=engine)
