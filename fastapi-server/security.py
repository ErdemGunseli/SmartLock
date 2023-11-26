from config import read_config

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# Indicating that we want to use the bcrypt hashing algorithm:
# Setting deprecated to "auto" means that any password hashes that are not using bcrypt will be automatically updated.
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# A JWT needs an algorithm and secret key.
# Secret key should be a random string. This was generated using openssl rand -hex 32:
SECRET_KEY = read_config("SECRET_KEY")
ALGORITHM = "HS256"
# The time to live for the JWT:
TOKEN_TTL = timedelta(minutes=30)


def create_access_token(id: int, name: str, admin: bool, ttl: timedelta = TOKEN_TTL):
    expiry = datetime.utcnow() + ttl

    # The payload is the data that we want to encode within the token.
    # Tokens will be used by the server to understand which user is making the requests.
    # "sub" stands for the subject, and should be unique:
    payload = {"sub": name, "id": id, "admin": admin, "exp": expiry}

    # Creating the JWT, using the secret key and algorithm to encode the payload:
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)
