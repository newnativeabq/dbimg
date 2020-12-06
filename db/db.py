"""
Database
    Initialize and create connection control flow for database.
    Datase parameters must be set in config.py or directly in app.py
"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from decouple import config

import logging

from utils import g 

###############################
### SQL Database Connection ###
###############################
def get_db() -> sqlalchemy.engine:
    """
    Returns current database connection.  If connection not present,
    initiates connection to configured database.  Default is non-authenticated SQL.
    Modifty g.db = *connect to match intended database connection.
    """
    db_uri = config('DATABASE_URI')

    db_logger = logging.getLogger(__name__ + '.getdb')
    if not hasattr(g, 'db'):
        db_logger.info('DB connection not found. Attempting connection to {}.'.format(db_uri))
        try:
            g.engine = create_engine(db_uri)
            g.db = g.engine.connect()
        except:
            db_logger.error('Could not establish connection.  Aborting.')
            raise ConnectionError

    return g.db


@contextmanager
def get_session():
    # Setup session with thread engine.
    #   Allows for usage: with get_session() as session: session...
    engine = get_db()
    session = scoped_session(sessionmaker(bind=engine))
    try:
        yield session
    finally:
        session.close()


def close_db(e=None):
    db = get_session()
    if db is not None:
        db.close()


def init_db():
    db = get_db()


## SQL DB Utils ##

def query_db(query):
    db = get_db()
    return db.execute(query)