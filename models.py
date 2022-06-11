from email.policy import default
from enum import unique
from sqlalchemy import Boolean, Column, Integer, String

from .database import Base

# How your data should be stored in the database.
# 1. Define the URL class.
# 2. Define the __tablename__ attribute.
# 3. Define the id, key, secret_key, target_url, is_active, and clicks attributes.
# 4. Define the id column as the primary key.
# 5. Define the key column as a unique column and index it.
# 6. Define the secret_key column as a unique column and index it.
# 7. Define the target_url column as an index.
# 8. Define the is_active column as a default value of True.
# 9. Define the clicks column as a default value of 0.
class URL(Base):
    """A database model named URL

    Args:
        Base (class): `id` is the primary key of for the database.
        The `key` field contains random strings for the shortened URL.
        `secret_key` allows the user to manage their shortened URL and see statistics.
        `target_url` to store the URL strings for which the app provides shortened URLs.
        `clicks` starts with zero. This field will increase each time someone clicks the shortened link.
    """

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
