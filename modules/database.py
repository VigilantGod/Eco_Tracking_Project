from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import declarative_base,sessionmaker
import os

#creates the data directory if not exist
if not os.path.exists("data"):
    os.mkdir()

#database url
db_URL = "sqlite:///data/ecotrack.db"
#engine to connect to the database
engine = create_engine(db_URL)
session = sessionmaker(bind=engine)
base = declarative_base()

#Users table
class Users(base):
    __tablename__ = "users"

    username = Column(String,primary_key=True,index=True)
    password = Column(String(128),nullable=False)
    email = Column(String,nullable=False)
    phone_number = Column(String,nullable=True)


base.metadata.create_all(bind=engine)

def get_db():
    """
    Returns a session of the database
    """
    return session()

def  store_user(db,user:str,email:str,phone_number:str,hashed_password:str):
    """store a user details in the database"""
    new_user = Users(username=user,email=email,phone_number=phone_number,password=hashed_password)
    #add new_user to the temporary memory of db
    db.add(new_user)
    #permenently saving details
    db.commit()
    #reloads the db so it will get the most recent data
    db.refresh(new_user)
    return new_user
