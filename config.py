# It allows us to cache the results of a function call.
from functools import lru_cache

from pydantic import BaseSettings


# 1. It imports the BaseSettings class from the settings.py file.
# 2. It creates a new class called Settings that inherits from BaseSettings.
# 3. It defines the environment name, base_url, and db_url variables.
# 4. It calls the super().__init__() method to set the other variables.
# 5. It returns the Settings class.
class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

    class Config:
        env_file = ".env"


# 1. The decorator @lru_cache is a decorator that will cache the return value of the function.
# 2. The function get_settings() is a function that returns a Settings object.
# 3. The decorator @lru_cache will cache the return value of get_settings().
# 4. The function get_settings() is called twice.
# 5. The first time, the function get_settings() is called, it will return a Settings object.
# 6. The second time, the function get_settings() is called, the return value will be retrieved from the cache.
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading setting for: {settings.env_name}")
    return settings
