from random import choice
from cryptography.fernet import Fernet

def generate_code() -> str:
    """ Generate random verify code """
    password: str = ''
    numbers: tuple = ('1234567890')

    for _ in range(4):
        password += choice(choice(numbers))

    return password


def cryptography_fearnet_encoder(password: str) -> str:
    """ This function to encrypt password"""
    key = Fernet.generate_key()
    fernet = Fernet(key)
    
    encMessage = fernet.encrypt(password.encode())
    print(f"encMessage: {encMessage}, key: {key}")
    return encMessage, key

def cryptography_fearnet_decoder(password: str, key: str) -> str:
    """ This function to decrypt password"""
    fernet = Fernet(key)

    return fernet.decrypt(password).decode()
    
    