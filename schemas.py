# It creates a class that will be used to create objects that will be used
# to create a schema for the data that will be input.
from pydantic import BaseModel


# 1. The URLBase class inherits from BaseModel.
# 2. The URLBase class contains the field target_url, which requires a string.
# 3. The URLBase class stores the URL to be shortened.
class URLBase(BaseModel):
    """The URLBase class contains the field target_url,
    which requires a string. stores the URL to be shortened.

    Args:
        BaseModel (class): `target_url` stores the URL to be shortened.
    """

    target_url: str


# 1. Declares the URL class as a subclass of URLBase.
# 2. Declares the URL class’s fields.
# 3. Configures the URL class to use the SQLAlchemy ORM.
class URL(URLBase):
    """URL class inherits the `target_url` field from URLBase.
    Args:
        URLBase (class): The Boolean field `is_active` and the integer field `clicks`.
        The is_active field allows you to deactivate shortened URLs.
        `clicks` counts how many times a shortened URL has been visited.

    """

    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


# 1. The URLInfo class inherits from URL.
# 2. The URLInfo class has two new properties: url and admin_url.
# 3. The URLInfo class has two new methods: get_url() and get_admin_url().
# 4. The URLInfo class has two new decorators: @property and @staticmethod.
# 5. The URLInfo class has two new static methods: get_url_info() and get_admin_url_info().
class URLInfo(URL):
    url: str
    admin_url: str
