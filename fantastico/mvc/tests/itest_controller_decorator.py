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
.. py:module:: fantastico.mvc.tests.itest_controller_decorator
'''

from fantastico.routing_engine.dummy_routeloader import DummyRouteLoader
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from urllib.request import Request
import urllib
from urllib.error import HTTPError

class ControllerDecoratorIntegration(DevServerIntegration):
    '''This class provides the test cases that ensures controller decorator works as expected into integration environment.'''

    def init(self):
        self._response = None
        self._exception = None

    def test_route_registration(self):
        '''This test case ensures routes are registered correctly by Controller decorator.'''

        def request_logic(server):
            content_type = "application/html; charset=UTF-8"

            request = Request(self._get_server_base_url(server, DummyRouteLoader.DUMMY_ROUTE))
            request.headers["Content-Type"] = content_type

            with self.assertRaises(HTTPError) as cm:
                urllib.request.urlopen(request)

            self._exception = cm.exception

        def assert_logic(server):
            content_type = "application/html; charset=UTF-8"

            self.assertTrue(self._exception.read().decode().find("Hello world.") > -1)
            self.assertEqual(content_type, self._exception.info()["Content-Type"])

        self._run_test_against_dev_server(request_logic, assert_logic)

    def test_mvc_sample_hello_ok(self):
        '''This test case does an http request against mvc hello world controller. It proves that registration of routes
        mapped through decorators is working as expected.'''

        def request_logic(server):
            content_type = "text/html; charset=UTF-8"

            request = Request(self._get_server_base_url(server, "/mvc/hello-world"))
            request.headers["Content-Type"] = content_type

            self._response = urllib.request.urlopen(request)

        def assert_logic(server):
            content_type = "text/html; charset=UTF-8"

            self.assertTrue(200, self._response.getcode())
            self.assertTrue(self._response.read().decode().find("Hello world.") > -1)
            self.assertEqual(content_type, self._response.info()["Content-Type"])

        self._run_test_against_dev_server(request_logic, assert_logic)
