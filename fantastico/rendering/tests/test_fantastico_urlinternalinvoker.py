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
.. py:module:: fantastico.rendering.tests.test_fantastico_urlinternalinvoker
'''
from fantastico.exceptions import FantasticoUrlInvokerError
from fantastico.rendering.url_invoker import FantasticoUrlInternalInvoker
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class FantasticoUrlInternalInvokerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases that ensure correct behavior of url invoker for fantastico app internal urls.'''

    def init(self):
        '''This method is automatically invoked before running each test case.'''

        self._wsgi_environ = {}
        self._start_response_invoked = False

    def test_invoke_url_ok(self):
        '''This test case ensures invoke url works as expected.'''

        expected_response = ["simple response body"]
        expected_headers = [("CONTENT-TYPE", "application/json")]

        url = "/simple/url"
        headers = [("HTTP_CONTENT_TYPE", "application/json")]

        app = self._get_mock_app(self._wsgi_environ, expected_response, expected_headers)

        invoker = FantasticoUrlInternalInvoker(app, self._wsgi_environ)

        response = invoker.invoke_url(url, headers)

        self.assertEqual(expected_response, response)
        self.assertEqual(200, invoker.http_status)
        self.assertEqual(expected_headers, invoker.http_headers)

        return invoker

    def test_invoke_url_exception(self, invoker=None):
        '''This test case ensures invoke url internal exceptions are converted to concrete exceptions.'''

        app = Mock(side_effect=Exception("Unexpected exception"))

        if not invoker:
            invoker = FantasticoUrlInternalInvoker(app, self._wsgi_environ)

        invoker._app = app

        with self.assertRaises(FantasticoUrlInvokerError) as ex_ctx:
            invoker.invoke_url("/simle/url", [])

        self.assertTrue(str(ex_ctx.exception).find("Unexpected exception") > -1)

        return invoker

    def test_invoke_url_reset_headersstatus(self):
        '''This test case ensures subsequent invocation of urls using the same invoker instance reset headers and status
        correctly, making each request independent.'''

        invoker = self.test_invoke_url_ok()

        self.test_invoke_url_exception(invoker)

        self.assertIsNone(invoker.http_status)
        self.assertEqual([], invoker.http_headers)

    def _get_mock_app(self, wsgi_environ, expected_response, expected_headers):
        '''This method builds a mock callable wsgi application that correctly invokes start_response callback. It controls
        the expected values that must be returned. In addition it ensures that correct environ is invoked.'''

        def callable_app(environ, start_response):
            self.assertEqual(wsgi_environ, environ)

            start_response(200, expected_headers)

            return expected_response

        return callable_app
