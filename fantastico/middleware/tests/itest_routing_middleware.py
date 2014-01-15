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
.. py:module:: fantastico.middleware.tests.itest_routing_middleware
'''
from fantastico.exceptions import FantasticoNoRequestError
from fantastico.middleware.routing_middleware import RoutingMiddleware
from fantastico.routing_engine.dummy_routeloader import DummyRouteLoader
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from mock import Mock
from webob.request import Request

class RoutingMiddlewareIntegration(FantasticoIntegrationTestCase):
    '''This class provides the test suite for making sure routing middleware correctly works with fantastico router.'''

    _routing_middleware = None

    def init(self):
        self._routing_middleware = RoutingMiddleware(Mock())

    def cleanup(self):
        self._routing_middleware = None

    def test_route_handling_ok(self):
        '''This test case makes sure an existing route is correctly handled.'''

        request = Request.blank(DummyRouteLoader.DUMMY_ROUTE)

        environ = request.environ
        environ["fantastico.request"] = request

        self._routing_middleware(environ, Mock())

        route_handler = environ.get("route_%s_handler" % DummyRouteLoader.DUMMY_ROUTE)

        self.assertIsNotNone(route_handler)
        self.assertIsInstance(route_handler.get("controller"), DummyRouteLoader)
        self.assertEqual("display_test", route_handler.get("method"))

    def test_route_handling_before_requestbuild(self):
        '''This test cases ensures that a fantastico exception is thrown if RequestMiddleware was not executed before.'''

        request = Request.blank(DummyRouteLoader.DUMMY_ROUTE, environ=None)

        environ = request.environ

        self.assertRaises(FantasticoNoRequestError, self._routing_middleware, *[environ, Mock()])
