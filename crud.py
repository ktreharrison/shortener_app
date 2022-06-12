# 1. Importing the SQLAlchemy modules we’ll need.
# 2. Importing our models and schema modules.
from sqlalchemy.orm import Session
from . import keygen, models, schemas


# 1. Create a new URL object
# 2. Add the URL to the database
# 3. Commit the database session
# 4. Refresh the database object
# 5. Return the database object
def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """Create URL in the database

    Args:
        db (Session): Connect to a database
        url (schemas.URLBase): url to be shortened

    Returns:
        models.URL: return a shorten URL
    """
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


# 1. Import the models.URL class from the models module.
# 2. Import the get_db_url_by_key function from the db_utils module.
# 3. Create a new function called get_url_by_key that takes in a db session and a url_key.
# 4. Query the database for a URL with the provided url_key and is_active set to True.
# 5. Return the first result.
def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """This function returns either None or a database entry with a provided key.

    Args:
        db (Session): Connect to a database
        url_key (str): url key stored in database

    Returns:
        models.URL: return a json of the URL
    """
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


# 1. Import the models module from the models.py file.
# 2. Create a function that takes in a database session and a secret_key.
# 3. Query the database for an active URL entry with the provided secret_key.
# 4. Return the URL entry. Otherwise, return None.
def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """Checks your database for an active database entry
    with the provided secret_key.

    Args:
        db (Session): Connect to a database
        secret_key (str): url secret key stored in database

    Returns:
        models.URL: return an URL entry. Otherwise, returnd None.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


# 1. Import the SQLAlchemy Session
# 2. Import the URL model
# 3. Import the URL schema
# 4. Define a function that takes in a SQLAlchemy Session, and a URL in the database.
# 5. Increase the URL clicks value by one.
# 6. Commit the changes to the database.
# 7. Refresh the database with the latest values.
# 8. Return the updated URL.
def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """Increase the URL clicks value by one.

    Args:
        db (Session): Connect to a database
        db_url (schemas.URL): an URL in the database

    Returns:
        models.URL: increase count by 1
    """
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


# 1. First, we get the URL by the `secret_key` from the database.
# 2. If the URL is found, we set the `is_active` attribute to False.
# 3. We commit the changes to the database.
# 4. We refresh the database object to get the latest data.
# 5. We return the database object.
def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """Deactivates a URL by the `secret_key`

    Args:
        db (Session): _description_
        secret_key (str): _description_

    Returns:
        models.URL: set the `is_active` attribute to False
    """
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
