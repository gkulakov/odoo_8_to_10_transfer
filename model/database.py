# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, event
from contextlib import contextmanager
import time
import logging

logging.basicConfig()
logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.INFO)


class DataAccessLayer:

    def __init__(self):
        self.engine = None
        self.newSession = None
        self.session = None

    def connect(self, db_user, db_pass, db_address, db_name):
        self.engine = create_engine(
            'postgresql+psycopg2://{}:{}@{}/{}'.format(
                db_user, db_pass, db_address, db_name
            ), pool_recycle=300)
        # self.engine.echo = True
        self.newSession = sessionmaker(bind=self.engine)
        self.session = self.newSession()

    @contextmanager
    def session_context(self):
        """Provide a transactional scope around a series of operations."""
        session = self.newSession()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def translate(self, tbl, cond):
        # s = self.session
        result = self.session.query(tbl).filter(cond).first()
        # s.close()
        return result[0]


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    logger.debug("Start Query: \n%s", statement)
    logger.debug("Query arguments: %s", parameters)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    logger.debug("Query Complete!")
    logger.debug("Total Time: %f", total)
