# 1. Importing the sqlite3 module.
# 2. Importing the sqlalchemy module.
# 3. Importing the declarative_base module from sqlalchemy.ext.declarative.
# 4. Importing the sessionmaker module from sqlalchemy.orm.
# 5. Calling the get_settings() function from the config module.
# 6. Creating a new SQLite database called data.db.
# 7. Creating a new SQLAlchemy engine called engine.
# 8. Creating a new SQLAlchemy declarative base called Base.
# 9. Creating a new SQLAlchemy session called session.
from sqlite3 import connect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

# Entry point to database
# 1. Importing the create_engine function from the sqlalchemy module.
# 2. Creating an engine object with the database URL from the settings file.
# 3. Connecting to the database using the connect_args argument.
engine = create_engine(
    # The database URL from db_url of the settings
    get_settings().db_url,
    connect_args={"check_same_thread": False},
)
# Create a Local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# connects the database engine to the SQLAlchemy functionality of the models
# It creates a base class that our class code will inherit from.
Base = declarative_base()
