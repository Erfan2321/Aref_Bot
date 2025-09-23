import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
eng = create_engine(os.getenv("DATABASE_URL"))

with eng.begin() as conn:
    print("DB OK? ->", conn.execute(text("SELECT 1")).scalar())
    rows = conn.execute(text("""
        SELECT telegram_id, firstname, lastname, phone, grade, field, city, updated_at
        FROM users ORDER BY updated_at DESC LIMIT 5
    """)).all()
    for r in rows:
        print(r)
