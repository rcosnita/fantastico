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
.. py:module:: fantastico.oauth2.tokens_middleware
'''
from fantastico import mvc
from fantastico.exceptions import FantasticoNoRequestError, FantasticoDbError
from fantastico.oauth2.security_context import SecurityContext
from fantastico.oauth2.tokens_service import TokensService

class OAuth2TokensMiddleware(object):
    '''This class provides a middleware responsible for decoding an access token (if exists) and building a security context. It
    is extremely import to configure this middleware to run after
    :py:class:`fantastico.middleware.request_middleware.RequestMiddleware` and after
    :py:class:`fantastico.middleware.model_session_middleware.ModelSessionMiddleware` because
    it needs a valid request and connection manager saved in the current pipeline execution.'''

    TOKEN_QPARAM = "token"
    AUTHORIZATION_FORMAT = "Bearer %s"

    def __init__(self, app, tokens_service_cls=TokensService):
        self._app = app
        self._tokens_service_cls = tokens_service_cls

    def __call__(self, environ, start_response, conn_manager=mvc):
        '''This method is invoked automatically during middleware pipeline execution. For tokens middleware, this is the place
        where oauth2 access tokens are decrypted and validated.'''

        request = environ.get("fantastico.request")
        if not request:
            raise FantasticoNoRequestError("OAuth2TokensMiddleware must execute after RequestMiddleware.")

        if not conn_manager.CONN_MANAGER:
            raise FantasticoDbError(msg="OAuth2TokensMiddleware must execute after ModelSessionMiddleware.")

        db_conn = conn_manager.CONN_MANAGER.get_connection(request.request_id)

        encrypted_token = request.params.get(self.TOKEN_QPARAM, self._get_token_from_header(request))
        if not encrypted_token:
            request.context.security = SecurityContext(None)
            return self._app(environ, start_response)

        request.context.security = self._build_security_context(encrypted_token, db_conn)

        return self._app(environ, start_response)

    def _build_security_context(self, encrypted_token, db_conn):
        '''This method builds a security context using the current encrypted token and the currently opened db connection.'''

        tokens_service = self._tokens_service_cls(db_conn)
        token = tokens_service.decrypt(encrypted_token)
        tokens_service.validate(token)

        return SecurityContext(token)

    def _get_token_from_header(self, request):
        '''This method retrieves the oauth2 bearer token from request. If the token is not found None is returned.'''

        authorization = request.headers.get("Authorization")

        if not authorization:
            return

        auth_parts = authorization.split(" ")

        if len(auth_parts) < 2 or auth_parts[0] != "Bearer":
            return None

        return " ".join(auth_parts[1:])
