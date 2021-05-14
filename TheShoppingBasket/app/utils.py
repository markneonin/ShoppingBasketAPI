import os
from hashlib import pbkdf2_hmac, sha256


def generate_secure_data(pswd):
    salt = os.urandom(16)

    pswd_key = pbkdf2_hmac(
        hash_name='sha256',
        password=pswd.encode('utf-8'),
        salt=salt,
        iterations=100000)

    api_secret, api_secret_key = generate_api_secret(salt)

    return salt, pswd_key, api_secret, api_secret_key


def generate_api_secret(salt):
    base = os.urandom(16)
    api_secret = sha256(base).hexdigest()
    api_secret_key = pbkdf2_hmac(
        hash_name='sha256',
        password=api_secret.encode('utf-8'),
        salt=salt,
        iterations=100000)

    return api_secret, api_secret_key

