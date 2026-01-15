import streamlit as st
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from modules import database
import re
from modules import encrypt

psw_hasher = PasswordHasher()

def create_user(full_name:str,username:str,email:str,phone_number:str,password:str,is_admin:bool=False):
    """Cretaes a User"""
    hashed_password = hash_password(password=password)
    db = database.get_db()

    database.store_user(
        db,
        full_name=full_name,
        user=username,
        email=email,
        phone_number=phone_number,
        hashed_password=hashed_password,
        is_admin=is_admin
        )


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
    try:
        return psw_hasher.hash(password)
    except Exception as e:
        st.error(f"Error hashing password: {e}")
        return None

def verify_password(txt_password:str,hashed_pass:str):
    """
    verifies a password
    """
    try:
        return psw_hasher.verify(hashed_pass, txt_password)
    except VerifyMismatchError:
        return False
    except Exception as e:
        st.error(f"Error verifying password: {e}")
        return False


