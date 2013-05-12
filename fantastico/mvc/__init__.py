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
'''

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

BaseModel = declarative_base()
Session = None

engine = None

def init_dm_db_engine(db_config, echo=False):
    '''Method used to configure the SQL Alchemy ORM behavior for Fantastico framework. It must be executed once per wsgi
    fantastico worker.'''

    global engine, Session

    conn_props = {"drivername": db_config["drivername"],
                  "username": db_config["username"],
                  "password": db_config["password"],
                  "host": db_config["host"],
                  "port": db_config["port"],
                  "database": db_config["database"],
                  "query": db_config["additional_params"]}

    if not engine and isinstance(conn_props, dict):
        conn_data = URL(**conn_props)
        engine = create_engine(conn_data, echo=echo)

        Session = scoped_session(sessionmaker(bind=engine))