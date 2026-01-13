from modules import database,encrypt,auth
import getpass


def create_admin_account():
    print("Create Admin Account")
    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")
    email = input("Enter admin email: ")
    full_name = input("Enter full name: ")
    phone_number = input("Enter phone number: ")

    db = database.get_db()
    
    existing_admin =  db.query(database.Users).filter(database.Users.username == username).first()

    if existing_admin:
        print("Admin username already exists")
        return
    
    enc_full_name = full_name
    enc_phone_number = phone_number
    enc_email = email
    hashed_password = auth.hash_password(password)

    database.store_user(
        db,
        full_name=enc_full_name,
        user=username,
        email= enc_email,
        phone_number=enc_phone_number,
        hashed_password=hashed_password,
        is_admin=True
    )

def main():
    create_admin_account()
    print("Admin account created successfully.")

if __name__ == "__main__":
    main()
