from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g 

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URI'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
    Base.metadata.create_all(engine)
    app.teardown_appcontext(close_db_session)

def start_db_session():
    # only makes a new sessions if one is not already in progress
    if 'db' not in g:
        # store db connection in app context(global)
        g.db = Session()
    
    return g.db


def close_db_session(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

