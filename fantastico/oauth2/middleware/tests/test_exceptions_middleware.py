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
.. py:module:: fantastico.oauth2.middleware.tests.test_exceptions_middleware
'''
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError, OAuth2AuthenticationError, OAuth2InvalidClientError, \
    OAuth2Error
from fantastico.oauth2.middleware.exceptions_middleware import OAuth2ExceptionsMiddleware
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from webob.util import status_reasons
import json

class ExceptionsMiddlewareTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for OAuth2 exceptions handler.'''

    _DOC_BASE = "/test/documentation/"

    def test_invalid_request(self):
        '''This test case ensures the correct json response is built when a mandatory parameter is missing.'''

        ex = OAuth2MissingQueryParamError("username")

        body = self._test_exception_json(ex)

        self._assert_error_response(error="invalid_request",
                                    description="username query parameter is mandatory.",
                                    uri=self._calculate_expected_uri(ex.error_code),
                                    body=body)

    def test_access_denied(self):
        '''This test case ensures oauth2 authentication exceptions are correctly converted to access denied responses.'''

        ex = OAuth2AuthenticationError("Username or password are not correct.")

        body = self._test_exception_json(ex)

        self._assert_error_response(error="access_denied",
                                    description=str(ex),
                                    uri=self._calculate_expected_uri(ex.error_code),
                                    body=body)

    def test_invalid_client(self):
        '''This test case ensures oauth2 invalid client exceptions are correctly converted to access denied responses.'''

        ex = OAuth2InvalidClientError("Invalid client error.")

        body = self._test_exception_json(ex)

        self._assert_error_response(error="invalid_client",
                                    description=str(ex),
                                    uri=self._calculate_expected_uri(ex.error_code),
                                    body=body)

    def test_server_error(self):
        '''This test case ensures generic oauth2 errors are casted to internal server error.'''

        ex = OAuth2Error(error_code=232, msg="Unexpected error", http_code=500)

        body = self._test_exception_json(ex)

        self._assert_error_response(error="server_error",
                                    description=str(ex),
                                    uri=self._calculate_expected_uri(ex.error_code),
                                    body=body)


    def test_generic_exception(self):
        '''This test case ensures non oauth2 exceptions are bubbled up.'''

        ex = Exception("Unexpected exception")

        with self.assertRaises(Exception) as ctx:
            self._test_exception_json(ex)

        self.assertEqual(ex, ctx.exception)

    def _assert_error_response(self, error, description, uri, body):
        '''This method assert correct exception format response for the given body.'''

        self.assertEqual(error, body.get("error"))
        self.assertEqual(description, body.get("error_description"))
        self.assertEqual(uri, body.get("error_uri"))

    def _calculate_expected_uri(self, error_code):
        '''This method calculates expected uri for the given error code.'''

        return "%sfeatures/oauth2/exceptions/%s.html" % (self._DOC_BASE, error_code)

    def _test_exception_json(self, ex):
        '''This method provides a template test case for ensuring invalid request error response is correctly built.'''

        request = Mock()
        request.content_type = "text/plain"

        environ = {"fantastico.request": request}
        start_response = Mock()
        app = Mock(side_effect=ex)
        middleware = OAuth2ExceptionsMiddleware(app, settings_facade_cls=self._mock_settings_facade())

        body = middleware(environ, start_response)

        self.assertIsNotNone(body)

        content_length = len(body[0])
        body = json.loads(body[0].decode())

        app.assert_called_once_with(environ, start_response)

        http_code = ex.http_code

        if http_code >= 500:
            http_code = 400

        http_code = "%s %s" % (http_code, status_reasons[http_code])
        start_response.assert_called_once_with(http_code, [("Content-Type", "application/json; charset=UTF-8"),
                                                           ("Content-Length", str(content_length))])

        return body

    def _mock_settings_facade(self):
        '''This method mocks settings facade.'''

        settings_facade = Mock()
        settings_facade.get = Mock(return_value=self._DOC_BASE)
        settings_facade_cls = Mock(return_value=settings_facade)

        return settings_facade_cls
