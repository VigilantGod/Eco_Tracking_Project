from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv,set_key
import base64
import os

#masterkry is stored in .env
env_path = ".env"
load_dotenv(env_path)
master_key = os.getenv("ENCRYPTION_KEY")

if not master_key:
    master_key = AESGCM.generate_key(bit_length=256)
    set_key(
        env_path,
        "ENCRYPTION_KEY",
        base64.urlsafe_b64encode(master_key).decode('utf-8')
        )
    print("Since No master key found New key added to .env")

else:
    master_key = base64.urlsafe_b64decode(master_key)

aesgcm = AESGCM(master_key)

def encrypt_data(data:str)->bytes:
    """
    Encrypts data
    input:
        plain data(str)
    returns:
        nonce(number used once) + encypted data (dtype= bytes)
    """
    if data is None:
        return None
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce,data=data.encode("utf-8"),associated_data=None)
    return nonce + encrypted

def decrypt_data(encrypted_with_nonce:bytes)-> str:
    """
    Decrypts data
    input:
        encrypted data with nonce
    return:
        decrypted data(str)
    """
    #since only used 12 digit nonce
    if encrypted_with_nonce is None:
        return None
    nonce,encrypted_data = encrypted_with_nonce[:12],encrypted_with_nonce[12:]

    return aesgcm.decrypt(nonce=nonce,data = encrypted_data,associated_data=None).decode("utf-8")