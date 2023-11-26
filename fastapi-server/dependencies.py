from database import SessionLocal
from security import SECRET_KEY, ALGORITHM, bcrypt_context
from config import read_config
from models import User



from starlette import status as st
from fastapi import Depends, HTTPException
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


def get_db():
    # Using a generator as a context manager to create and maintain a database connection:

    # Instantiating the SessionLocal class (created in database.py) to connect to the database,
    # where db represents a database connection:
    db = SessionLocal()
    try:
        # Returning the connection using the "yield" keyword means that the database will not be closed before
        # the calling function finishes.
        yield db
    finally:
        # The code following the "yield" statement will run once the function that calls get_db finishes.
        db.close()


# The argument of "Depends" specifies which function should be called for the dependency injection.
# The "Annotated" class allows us to add additional metadata to type hints.
# In this case, the return value of get_db is of type Session.
db_dependency = Annotated[Session, Depends(get_db)]

# For the authentication dependency, the OAuth2PasswordRequestForm class must be instantiated:
auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]

# Instantiating OAuth2PasswordBearer with the token-generating endpoint kwarg:
token_dependency = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="auth/token"))]


async def get_current_user(token: token_dependency):
    # Error catching in case token is invalid:
    try:
        # Attempting to decode the token using the secret key and algorithm:
        # If successful, this will return a dictionary that contains the user data.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extracting the data from the payload dictionary:
        name: Optional[str] = payload.get("sub")
        id: Optional[int] = payload.get("id")
        admin: Optional[bool] = payload.get("admin")

    except JWTError:
        raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Error When Decoding JWT")

    if None in (id, name, admin): raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED,
                                                      detail="Invalid Credentials")
    return {"id": id, "name": name, "admin": admin}

# The get_current_user depends on the token_dependency, so just injecting the user_dependency will also inject the token_dependency:
user_dependency = Annotated[dict, Depends(get_current_user)]


def admin_setup():
    # An admin is necessary to create users, so creating an admin based on the config file:

    # Not using dependency injection for db:
    db = SessionLocal()

    # Need to be explicit about the condition, even though User.admin is boolean:
    admin = db.query(User).filter((User.admin == True)).first()

    # If there already is an admin, no need for further action:
    if admin: return

    # If there is no admin, creating one based on the config file:
    admin = User(name=read_config("ADMIN_NAME"), 
                 key=bcrypt_context.hash(read_config("ADMIN_KEY")), 
                 admin=True)
    db.add(admin)
    db.commit()
    db.close()


async def get_current_admin(user: user_dependency):
    if not user.get("admin"): 
        raise HTTPException(status_code=st.HTTP_403_FORBIDDEN, detail="Admin Access Required")
    return user

# The admin dependency depends on the user and token dependencies as well, so injecting it will also inject those.
admin_dependency = Annotated[dict, Depends(get_current_admin)]
