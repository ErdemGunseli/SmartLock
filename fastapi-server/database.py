from config import read_config

# A database engine is a way of connecting to the database - an intermediary between the Python code and the database.
from sqlalchemy import create_engine

# The session maker class is used to create session objects to manage connections to the database.
from sqlalchemy.orm import sessionmaker

# The declarative_base function is used to create a base class for declarative class definitions.
from sqlalchemy.orm import declarative_base


# 'postgresql' indicates that this is a PostgreSQL database.
# 'postgres' is the superuser name that is set as the owner of the database.
# 'localhost' is the host of the database.
# '5432' is the port number on which PostgreSQL is listening.
# 'SmartLockDatabase' is the name of the database.
DB_URL = f"postgresql://postgres:{read_config('POSTGRES_PASSWORD')}@localhost:5432/SmartLockDatabase"

# Creating the database engine:
engine = create_engine(DB_URL)

# Creating a SessionLocal class, used for creating session objects.
# auto commit = False means that the database will not automatically commit changes, manual commits are required.
# auto flush = False means that the session's changes to the database won't be synchronised automatically.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating a base class to be used by the data models:
Base = declarative_base()
