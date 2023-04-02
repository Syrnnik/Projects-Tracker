import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

links_icon_dir = os.path.join(os.getcwd(), "tmp/links_icons/")
if not os.path.exists(links_icon_dir):
    os.makedirs(links_icon_dir)

valid_icon_file_types = ["image/png", "image/jpeg", "image/bmp", "image/svg+xml"]


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
