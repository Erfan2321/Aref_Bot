# python create_db.py
from db import engine, Base
from db import models  # noqa: F401

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created/verified.")
