import bcrypt
from modules import database

def create_user(username:str,password:str):
    """Cretaes a User"""
    hashed_password = hash_password(password=password).decode("utf-8")
    db = database.get_db()

    database.store(username,hashed_password)

def hash_password(password:str):
    """
    Hashes the password
    """
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode("utf-8")

def verify_password(txt_password,hashed_pass):
    """
    verifies a password
    """
    return bcrypt.checkpw(txt_password.encode('utf-8'),hashed_pass)


