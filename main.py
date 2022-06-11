# 1. Importing the required libraries.
# 2. Importing the models and schemas from the models and schemas modules.
# 3. Creating a SessionLocal class to create a database session.
# 4. Creating a get_db function to return a database session.
# 5. Creating a get_settings function to return the settings.
# 6. Creating a FastAPI instance.
# 7. Adding the staticfiles directory to the FastAPI instance.
# 8. Creating a RedirectResponse to the index page.
# 9. Creating a HTMLResponse to the index page.
# 10. Creating a get_index function to return the index page.
import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from . import crud, models, schemas
from .database import SessionLocal, engine



# It gets the base URL from the admin config and then replaces the path with the key.
# 1. First, we get the base URL from the settings.
# 2. Then, we create a URL object from the base URL.
# 3. We create an admin endpoint from the app.
# 4. We replace the path of the base URL with the admin endpoint.
# 5. We return the URL object.
def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """Get baseline URL from admin config

    Args:
        db_url (models.URL): task the database URL

    Returns:
        schemas.URLInfo: returns a json object with deatails about the URL
    """
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for("administration info", secret_key=db_url.key)
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


# It creates a new FastAPI application object.
app = FastAPI()

# It tells the application that the static files are located in the static directory
app.mount("/static", StaticFiles(directory="./shortener_app/static"), name="static")


# This code creates a database file in the directory of your choosing. Binds the database engine
models.Base.metadata.create_all(bind=engine)


# 1. The get_db() function returns a new database session each time it is called.
# 2. The try … finally block ensures that the database connection is always closed, even if an error occurs.
# 3. The yield keyword in the get_db() function is what makes this function a generator.
# 4. The yield keyword pauses the function saving all its states and later continues from there on successive calls.
# 5. The get_db() function is a factory function that constructs the database connection and returns it.
# 6. The get_db() function is a factory function that constructs the database connection and returns it.
def get_db():
    """Connect to a SQLite Database

    Yields:
        class: new database sessions.
        The try … finally block to close the database conection
        in any case, even when an error occurs during the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


# main point of interaction
# This code is a simple HTML page that welcomes the user to the URL shortener API.
@app.get("/", response_class=HTMLResponse)
def read_root():
    """The root path and delegates all incoming GET requests

    Returns:
        str: Welcomes user to the URL shortener App.
    """

    return """
<html lang="en">
<head>
    <title>Ken's URL Shortener </title>
    <style>
        .img {
            text-align: center;
        }
    </style>
</head>
<body>
    <br>
    <h1 style="text-align: center">Welcome to the URL shortener API :)</h1>
    <div class="img">
        <img src="static/undraw_link_shortener_mvf6.svg" width="500" height="600">
    </div>
    <p style="text-align: center">by Ken Harrison</p>
</body>
</html>
"""


# 1. First, we import the HTTPException class from fastapi.exceptions.
# 2. Then, we define a function raise_bad_request that takes in a message as an argument and raises an HTTPException with a status code 400.
# 3. Finally, we raise an HTTPException with a status code 400 when the provided URL is not valid.
def raise_bad_request(message):
    """Use to validate bad request.

    Args:
        message (str): message as an argument
    and raises an HTTPException with a status code 400

    Raises:
        HTTPException:  raised when the provided URL is not valid
    """

    raise HTTPException(status=400, detail=message)


# 1. The first thing you do is create a URLInfo object that matches the
#    URLInfo schema.
# 2. You then check if the URL is valid. If it’s not, you raise a
#    BadRequest exception.
# 3. If the URL is valid, you create a database entry for the URL.
# 4. You then add the key and secret_key to the db_url to match the
#    required URLInfo schema that you need to return at the end of the
#    function.
# 5. You return the URLInfo object.
@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """Create a URL to be shortened

    Args:
        url (schemas.URLBase): Expects a URL string as a POST request body.
        By passing get_db into Depends(), you establish a database session
        for the request and close the session when the request is finished

        db (Session, optional): _description_. Defaults to Depends(get_db()).

    Returns:
        _type_: _description_
    """
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    # create a database entry for your target_url.
    db_url = crud.create_db_url(db=db, url=url)

    # adds key and secret_key to db_url to match the required URLInfo
    # schema that you need to return at the end of the function.
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return get_admin_info(db_url)


# 1. First, it checks if the URL exists in the database.
# 2. If it does, it returns the URL.
# 3. If it doesn’t, it raises an HTTPException with a 404 status code and a message.
def raise_not_found(request):
    """Error if key does not match any URLs in the database

    Args:
        request (str): a URL as a string

    Raises:
        HTTPException:  404 HTTP status code. URL does not exist
    """
    message = f"URL '{request.url}' doesnt exist"
    raise HTTPException(status_code=404, detail=message)


# 1. The @app.get decorator is used to register the URL path and HTTP verb for the function.
# 2. The function takes the URL key as a path parameter and a Request object as a dependency.
# 3. The function looks up the URL entry in the database using the URL key.
# 4. If the URL entry is found, the function updates the clicks count in the database and returns a RedirectResponse object.
# 5. If the URL entry is not found, the function raises a NotFound exception.
@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """_summary_

    Args:
        url_key (str): URL key in database
        request (Request): looks for an active URL entry in the database.
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        str: return the targeted URL
    """

    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)



# It gets the information about a URL from the database.
# 1. First, it checks if the URL exists in the database. If it does, it returns the URL information.
# 2. If the URL does not exist, it raises a 404 error.
@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """Function to get information about a URL

    Args:
        secret_key (str): Secret key of URL
        request (Request): body of the request
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """    
    if db_url := crud.get_db_url_by_secret_key(db=db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)


# 1. First, it checks if the secret key is valid. If it is, it deactivates the URL.
# 2. If the secret key is not valid, it raises a 404 error.
# 3. If the secret key is valid, it returns a message.
# 4. If the secret key is not valid, it raises a 404 error.
@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """Deactivates URL 

    Args:
        secret_key (str):  Secret key of URL
        request (Request): body of the request
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        str: A message if shortened URL was Successfully deleted, if not a 404 error
    """    
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key):
        message = f"Successfully deleted shortened URL for '{db_url}'"
        return {"deatail": message}
    else:
        raise_not_found(request)
