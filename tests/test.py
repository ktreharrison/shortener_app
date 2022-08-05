from shortener_app.config import get_settings
from shortener_app.database import SessionLocal
from shortener_app.keygen import create_random_key
from shortener_app.models import URL

# Test Setting
print(get_settings().base_url)
print(get_settings().db_url, end="\n\n\n")

# Test database connect
db = SessionLocal()


print(db.query(URL).all())
print(db.query(URL.secret_key).all(), end="n\n\n")

# Test random key generator
print(f" Random Generated Key: {create_random_key(10)}")
