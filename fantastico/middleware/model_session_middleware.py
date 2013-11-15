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
.. py:module:: fantastico.middleware.model_session_middleware
'''

from fantastico import mvc
from fantastico.settings import SettingsFacade

class ModelSessionMiddleware(object):
    '''This class is responsible for managing database connections across requests. It also takes care of
    connection data pools. By default, the middleware is automatically configured to open a connection. If
    you don't need mvc (really improbable but still) you simply need to change your project active settings
    profile. You can read more on :py:class:`fantastico.settings.BasicSettings`'''

    def __init__(self, app, settings_facade=SettingsFacade):
        self._app = app
        self._settings_facade = settings_facade()

    def __call__(self, environ, start_response, create_engine=None, create_session=None):
        '''This method actively creates a db session class ready to be used. Create_ parameters are here
        only for easing dependency injection and unit testing. You should not use them.'''

        db_config = self._settings_facade.get("database_config")

        mvc.CONN_MANAGER = mvc.init_dm_db_engine(db_config, echo=db_config.get("show_sql", False),
                                                 create_engine_fn=create_engine, create_session_fn=create_session)

        return self._app(environ, start_response)
