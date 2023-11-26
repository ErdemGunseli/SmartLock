import models
from dependencies import admin_setup
from database import engine
from routers import auth, actions

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# To run the server:
# cd fastapi-server
# source fastapienv/bin/activate
# uvicorn main:app --reload

# Setting up the app:
app = FastAPI()

# Enabling CORS (Cross-Origin Resource Sharing) to allow requests from the frontend:
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creating the database tables, passing the engine which is used to connect to the database:
models.Base.metadata.create_all(bind=engine)

# Checking that there is an admin and if not, creating one based on config data:   
admin_setup()

app.include_router(auth.router)
app.include_router(actions.router)


