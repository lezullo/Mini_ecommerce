from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = Path(__file__).resolve().parent
SQLALCHEMY_DATABASE_URL = f'sqlite:///{DB_PATH}/database.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
metadata = Base.metadata

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()