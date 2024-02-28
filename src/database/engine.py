import os
from contextlib import contextmanager
from sqlalchemy import create_engine, String
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker, Session
from .models import Base
db_path = 'sqlite:///db.sqlite3'
engine = create_engine(db_path,connect_args={'check_same_thread': False})


# Create the tables in the database
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
