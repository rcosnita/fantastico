'''
Copyright 2013 Cosnita Radu Viorel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. codeauthor:: Radu Viorel Cosnita <radu.cosnita@gmail.com>
.. py:module:: fantastico.mvc
'''

from fantastico.exceptions import FantasticoDbError
from fantastico.utils.singleton import Singleton
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

BASEMODEL = declarative_base()

class DbSessionManager(object):
    '''This class is responsible for managing db connections for fantastico framework. The current strategy implemented
    is based on a request id. This means once a request is done, it receives a request identifier which remains constant
    for the whole request.'''

    ENGINE = None
    SESSION = None

    def __init__(self, db_config, echo=False, create_engine_fn=None, create_session_fn=None):
        try:
            self._conn_props = self._build_conn_props(db_config)
        except Exception as ex:
            raise FantasticoDbError(ex)

        self._echo = echo
        self._engine_params = db_config.get("additional_engine_settings", {})
        self._create_engine_fn = create_engine_fn
        self._create_session_fn = create_session_fn

        self._cached_conns = {}

    def _build_conn_props(self, db_config):
        '''This method is used to build the connection properties required for connecting to fantastico configured database.'''

        conn_props = {"drivername": db_config["drivername"],
                      "username": db_config["username"],
                      "password": db_config["password"],
                      "host": db_config["host"],
                      "port": db_config["port"],
                      "database": db_config["database"],
                      "query": db_config["additional_params"]}

        return conn_props

    def get_connection(self, request_id):
        '''This method is responsible for retrieving an active session for the given request.'''

        session = self._cached_conns.get(request_id)

        if session:
            return session

        try:
            conn_data = URL(**self._conn_props)

            if not DbSessionManager.ENGINE:
                DbSessionManager.ENGINE = self._create_engine_fn(conn_data,
                                                                 echo=self._echo, **self._engine_params)
                DbSessionManager.SESSION = sessionmaker(bind=DbSessionManager.ENGINE)

            session = self._create_session_fn(DbSessionManager.SESSION, lambda: request_id)

            self._cached_conns[request_id] = session

            return session
        except Exception as ex:
            self.close_connection(request_id)

            raise FantasticoDbError(ex)

    def close_connection(self, request_id):
        '''This method is used to close the active session for a given request. It is recommended to invoke this only
        once per request cycle. Fantastico framework does this automatically at the end of each request cycle so you don't have
        to call this manually.'''

        session = self._cached_conns.get(request_id)

        if not session:
            return

        session.remove()
        session.close()

        del self._cached_conns[request_id]

CONN_MANAGER = None

def init_dm_db_engine(db_config, echo=False, create_engine_fn=None, create_session_fn=None):
    '''Method used to configure the SQL Alchemy ORM behavior for Fantastico framework. It must be executed once per wsgi
    fantastico worker.'''

    create_engine_fn = create_engine_fn or create_engine
    create_session_fn = create_session_fn or scoped_session

    return Singleton()(DbSessionManager(db_config, echo, create_engine_fn, create_session_fn))
