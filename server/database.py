from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create the database engine
engine = create_engine('sqlite:///client_data.db', echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()

# Define the Client model
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    udp_port = Column(Integer, nullable=False)
    files = relationship('File', back_populates='client')

# Define the File model
class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='files')

# Create the tables
Base.metadata.create_all(engine)

# Insert sample data into the tables
client_data = [
    Client(name='Alice', ip='192.168.1.100', udp_port=5000),
    Client(name='Bob', ip='192.168.1.101', udp_port=5001)
]

file_data = [
    File(filename='file1.txt', client_id=1),
    File(filename='file2.txt', client_id=2)
]

session.add_all(client_data)
session.add_all(file_data)
session.commit()

print("Data stored successfully.")
