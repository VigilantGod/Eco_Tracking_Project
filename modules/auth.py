import streamlit as st
import bcrypt
from sqlalchemy import create_engine, Column, String, Integer, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntergrityError
import os

if not os.path.exists("data"):
    os.mkdir("data")

Database_URL = "sqlite://data/ecotrack.db"
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

def hash_password(password:str):
    """
    Hashes a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

def verify_password(txt_password,hashed_pass):
    """
    verifies a password against a hashed password
    """
    return bcrypt.checkpw(txt_password.encode('utf-8',hashed_pass))

