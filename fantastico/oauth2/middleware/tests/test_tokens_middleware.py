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
.. py:module:: fantastico.oauth2.middleware.tests.test_tokens_middleware
'''
from fantastico.exceptions import FantasticoNoRequestError, FantasticoDbError
from fantastico.middleware.request_context import RequestContext
from fantastico.oauth2.middleware.tokens_middleware import OAuth2TokensMiddleware
from fantastico.oauth2.security_context import SecurityContext
from fantastico.oauth2.token import Token
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class TokensMiddlewareTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for OAuth2TokensMiddleware class.'''

    FANTASTICO_REQUEST_NAME = "fantastico.request"

    _request = None
    _environ = None
    _app = None
    _middleware = None
    _tokens_service = None
    _tokens_service_cls = None

    _db_conn = None
    _conn_manager = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies for all test cases.'''

        self._request = Mock()
        self._request.request_id = 123
        self._request.context = RequestContext({}, "en-US")
        self._environ = {self.FANTASTICO_REQUEST_NAME: self._request}

        self._tokens_service = Mock()
        self._tokens_service_cls = Mock(return_value=self._tokens_service)

        self._db_conn = Mock()
        self._conn_manager = Mock()
        self._conn_manager.CONN_MANAGER = Mock()
        self._conn_manager.CONN_MANAGER.get_connection = Mock(return_value=self._db_conn)

        self._app = Mock()
        self._middleware = OAuth2TokensMiddleware(self._app, tokens_service_cls=self._tokens_service_cls)

    def test_middleware_ok_query(self):
        '''This test case ensures OAuth2TokensMiddleware executes correctly when configured according to spec (runs after all native
        Fantastico middlewares executed) and access token is sent in query parameter **token**.'''

        param_token = "encrypted token value"
        token = Token({"scopes": ["scope1", "scope2"]})

        self._request.params = {OAuth2TokensMiddleware.TOKEN_QPARAM: param_token}
        self._request.headers = {}

        self._test_middleware_template(param_token, token)

    def test_middleware_ok_header(self):
        '''This test case ensures OAuth2TokensMiddleware executes correctly when configured according to spec (runs after all native
        Fantastico middlewares executed) and access token is sent in header **Authorization**.'''

        param_token = "encrypted token value"
        token = Token({"scopes": ["scope1", "scope2"]})

        self._request.params = {}
        self._request.headers = {"Authorization": "Bearer %s" % param_token}

        self._test_middleware_template(param_token, token)

    def _test_middleware_template(self, param_token, token):
        '''This method provides a template for testing middleware template correct behavior.'''

        self._tokens_service.decrypt = Mock(return_value=token)
        self._tokens_service.validate = Mock(return_value=True)

        start_response = Mock()
        self._middleware(self._environ, start_response, conn_manager=self._conn_manager)

        self.assertTrue(hasattr(self._request.context, "security"))

        security_ctx = self._request.context.security
        self.assertIsInstance(security_ctx, SecurityContext)
        self.assertEqual(security_ctx.access_token, token)

        self._conn_manager.CONN_MANAGER.get_connection.assert_called_once_with(self._request.request_id)
        self._tokens_service_cls.assert_called_once_with(self._db_conn)
        self._tokens_service.decrypt.assert_called_once_with(param_token)
        self._tokens_service.validate.assert_called_once_with(token)
        self._app.assert_called_once_with(self._environ, start_response)

    def test_middleware_norequest(self):
        '''This test case ensures a Fantastico concrete exception is raised if request middleware did not execute.'''

        with self.assertRaises(FantasticoNoRequestError):
            self._middleware({}, Mock())

    def test_middleware_noconnection(self):
        '''This test case ensures a Fantastico concrete exception is raised if model session middleware did not execute.'''

        conn_manager = Mock()
        conn_manager.CONN_MANAGER = None

        with self.assertRaises(FantasticoDbError):
            self._middleware(self._environ, Mock(), conn_manager=conn_manager)

    def test_middleware_notokenparam(self):
        '''This test case ensures no token logic is executed if token parameter is missing from request.'''

        middleware = OAuth2TokensMiddleware(self._app)

        start_response = Mock()
        self._request.params = {}
        self._request.headers = {"Authorization": "Unknown_token_type "}

        result = middleware(self._environ, start_response, conn_manager=self._conn_manager)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(self._request.context, "security"))
        self.assertIsNone(self._request.context.security.access_token)

        self._app.assert_called_once_with(self._environ, start_response)

        self.assertEqual(self._app(self._environ, start_response), result)
