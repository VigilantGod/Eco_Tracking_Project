import bcrypt
from sqlalchemy import create_engine, Column, String, Integer, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
import os

if not os.path.exists("data"):
    os.mkdir("data")

Database_URL = "sqlite:///data/ecotrack.db"
engine = create_engine(Database_URL)
SeessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    username = Column(String,primary_key=True,index=True)
    password = Column(LargeBinary,nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    """
    Returns a new database session.
    """
    return SeessionLocal()

def create_user(db,username:str,password:str):
    """
    Creates a new user in the database.
    """
    hashed_password = hash_password(password)
    new_user = Users(username=username,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def hash_password(password:str):
    """
    Hashes a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

def verify_password(txt_password,hashed_pass):
    """
    verifies a password against a hashed password
    """
    return bcrypt.checkpw(txt_password.encode('utf-8'),hashed_pass)


