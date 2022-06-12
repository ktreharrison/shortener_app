# This code imports the secrets module and the string module.
import secrets
import string
from sqlalchemy.orm import Session
from . import crud


# 1. Import the secrets module.
# 2. Import the string module.
# 3. Create a string of all uppercase letters and numbers.
# 4. Create a variable to store the random key.
# 5. A loop to generate random characters from the string of characters.
# 6. Join the random characters together to create a random key.
# 7. Return the random key.
def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


# 1. First, it creates a random key using the create_random_key() function.
# 2. Then, it checks if the key already exists in the database.
# 3. If it does, it creates another random key and checks again.
# 4. If it doesn’t, it returns the key.
def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
