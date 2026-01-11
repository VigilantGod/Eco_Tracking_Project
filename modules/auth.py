import bcrypt
from modules import database
import re

def create_user(full_name:str,username:str,email:str,phone_number:str,password:str):
    """Cretaes a User"""
    hashed_password = hash_password(password=password)
    db = database.get_db()

    database.store_user(db,full_name=full_name,user=username,email=email,phone_number=phone_number,hashed_password=hashed_password)


def validate_phone_number(phone_number:str):
    """
    Validates if the phone number is valid or not
    """
    pattern = r"^\+?[0-9]{10,15}"
    return re.match(pattern=pattern,string=phone_number)

def validate_email(email:str):
    """validates a email"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern=pattern,string=email)

def hash_password(password:str):
    """
    Hashes the password
    """
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode("utf-8")

def verify_password(txt_password:str,hashed_pass:str):
    """
    verifies a password
    """
    return bcrypt.checkpw(txt_password.encode('utf-8'),hashed_pass.encode("utf-8"))


