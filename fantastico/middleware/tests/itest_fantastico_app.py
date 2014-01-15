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
.. py:module:: fantastico.middleware.tests.itest_fantastico_app
'''
from fantastico.middleware.fantastico_app import FantasticoApp
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from mock import Mock
from fantastico.routing_engine.dummy_routeloader import DummyRouteLoader
from fantastico.exceptions import FantasticoContentTypeError

class FantasticoAppIntegration(FantasticoIntegrationTestCase):
    '''Class used to make sure fantastico can correctly handle requests.'''

    _environ = None
    _middleware = None

    def init(self):
        self._environ = {"CONTENT_TYPE": "text/html; charset=UTF-8",
                           "HTTP_ACCEPT": "text/html;q=1,application/json;q=0.9",
                           "HTTP_ACCEPT_LANGUAGE": "ro-ro,en-US;q=0.8",
                           "HTTP_OAUTH_BEARER": "123",
                           "HTTP_HOST": "localhost:80",
                           "PATH_INFO": DummyRouteLoader.DUMMY_ROUTE,
                           "QUERY_STRING": "id=1",
                           "REQUEST_METHOD": "GET",
                           "SCRIPT_NAME": "",
                           "SERVER_NAME": "localhost",
                           "SERVER_PORT": "80",
                           "SERVER_PROTOCOL": "HTTP/1.1",
                           "wsgi.multiprocess": False,
                           "wsgi.multithread": False,
                           "wsgi.run_once": False,
                           "wsgi.url_scheme": 'http',
                           "wsgi.version": (1, 0)}

        self._middleware = FantasticoApp()

    def test_request_ok(self):
        '''This Test case ensures requests are handled correctly by fantastico app (all configured middleware are executed).'''

        self._environ["CONTENT_TYPE"] = "application/json"
        response = self._middleware(self._environ, Mock())

        self.assertIsNotNone(self._environ.get("fantastico.request"))
        self.assertEqual([b"Hello world."], response)

    def test_request_incompatible_content(self):
        '''This test case ensures request content type different than response content type raises an exception.'''

        self.assertRaises(FantasticoContentTypeError, self._middleware, *[self._environ, Mock()])

        self.assertIsNotNone(self._environ.get("fantastico.request"))
