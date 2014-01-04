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
.. py:module:: fantastico.oauth2.grant_handler_factory
'''
from fantastico.oauth2.exceptions import OAuth2UnsupportedGrantError
from fantastico.oauth2.implicit_grant_handler import ImplicitGrantHandler
from fantastico.oauth2.tokens_service import TokensService
from fantastico.settings import SettingsFacade

class GrantHandlerFactory(object):
    '''This class provides a factory which can be used to obtain a concrete grant handler. Below you can find a code snippet for
    obtaining and implicit grant type handler:

    .. code-block:: python

        grant_handler = GrantHandlerFactory().get_handler(GrantHandlerFactory.IMPLICIT_GRANT)'''

    IMPLICIT_GRANT = "token"

    def __init__(self, tokens_service_cls=TokensService, settings_facade_cls=SettingsFacade):
        self._supported_grants = {self.IMPLICIT_GRANT: ImplicitGrantHandler}
        self._tokens_service_cls = tokens_service_cls
        self._settings_facade = settings_facade_cls()

    def get_handler(self, handler_type, db_conn):
        '''This method builds a grant handler which matches requested handler_type.

        :param handler_type: A string value describing the grant_type which must be handled.
        :type handler_type: str
        :param db_conn: A db connection active session which cn be used.
        :type db_conn: Connection
        :returns: A concrete grant handler instance.
        :rtype: :py:class:`fantastico.oauth2.grant_handler.GrantHandler`
        '''

        handler_cls = self._supported_grants.get(handler_type)

        if not handler_cls:
            raise OAuth2UnsupportedGrantError(handler_type)

        tokens_service = self._tokens_service_cls(db_conn)

        return handler_cls(tokens_service, self._settings_facade)
