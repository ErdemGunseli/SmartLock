from models import User
from dependencies import db_dependency, auth_dependency, admin_dependency
from security import create_access_token, bcrypt_context

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status as st

router = APIRouter(prefix="/auth", tags=["auth"])


class CreateUserRequest(BaseModel):
    # ID will be auto-incremented, there can only be one admin:
    # Pydantic Field represents expected fields in the incoming data:
    name: str = Field(example="John Doe", minlength=2, max_length=50)
    key: str = Field(example="123456", min_length=6, max_length=50)

    class Config:
        title = "User Details"
        schema_extra = {
            # Do not modify the dictionary keys:
            "example": {
                "name": "",
                "key": ""
            }
        }


@router.post("/user", status_code=st.HTTP_201_CREATED)
async def create_user(user_input: CreateUserRequest, _: admin_dependency, db: db_dependency):

    users = db.query(User).all()

    # Checking if a user with the same name or access key already exists:
    for user in users:
        if bcrypt_context.verify(user_input.key, user.key) or (User.name == user_input.name):
            raise HTTPException(status_code=st.HTTP_409_CONFLICT, detail="User already exists")
        

    # Creating a new user object (ID is auto-incremented, admin is false by default):
    new_user = User(name=user_input.name, key=bcrypt_context.hash(user_input.key))

    # Adding the new user to the database:
    db.add(new_user)
    db.commit()


@router.get("/user/", status_code=st.HTTP_200_OK)
async def read_users(_: admin_dependency, db: db_dependency):
    return db.query(User).all()


@router.delete("/user/{user_id}", status_code=st.HTTP_200_OK)
async def delete_user(_: admin_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    # Searching for a user of the input ID:
    user = db.query(User).filter((user_id == User.id)).first()

    if user is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="User not found")
    if user.admin: raise HTTPException(status_code=st.HTTP_403_FORBIDDEN, detail="Cannot delete admin")

    # Deleting the user from the database:
    db.delete(user)
    db.commit()


def authenticate_user(key: str, db):
    # Every time that a string is hashed, it will produce a different result due to the salt.
    # So we cannot hash the input key and compare it to the hashed key in the database.

    # Obtaining a list of all users of the lock:
    users = db.query(User).all()
    for user in users:
        if bcrypt_context.verify(key, user.key): 
            return user
        
    raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Access key is incorrect")


@router.post("/token")
async def login_and_generate_token(user_input: auth_dependency, db: db_dependency):
    # user_input is of type OAuth2PasswordRequestForm, so it has attributes username and password.
    # For the smart lock, since there will be a handful of users, we don't need usernames to be entered:
    user = authenticate_user(user_input.password, db)

    # If the execution reaches this point, we know user is not None.
    token = create_access_token(user.id, user.name, user.admin)

    # 'bearer' indicates a request should be authenticated using the provided access token
    # i.e. it is a hint about how to use the token.
    # The return value uses the OATH2.0 Bearer Token Specification format:
    return {"access_token": token, "token_type": "bearer"}
