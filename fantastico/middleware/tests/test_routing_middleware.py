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
.. py:module:: fantastico.middleware.tests.test_routing_middleware
'''
from fantastico.exceptions import FantasticoNoRequestError, FantasticoError
from fantastico.middleware.routing_middleware import RoutingMiddleware
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from webob.request import Request

class RoutingMiddlewareTests(FantasticoUnitTestsCase):
    '''This class provides all test cases required to make sure routing middleware is working as expected.'''
    
    def init(self):
        self._environ = {}
        self._app = Mock()
        self._router = Mock()
        self._router_cls = Mock(return_value=self._router)
        self._routing_middleware = RoutingMiddleware(self._app, self._router_cls)
        
    def test_route_handled_correctly(self):
        '''This test case ensures a route is handled correctly using the middleware.'''
        
        self._environ["fantastico.request"] = Request.blank("/simple/request")
        
        def handle_route(url, environ):
            if url == "/simple/request":
                environ["route_/simple/request_handler"] = {"controller": SimpleController(), "method": "do_request"}
        
        self._router.handle_route = handle_route
        
        self._routing_middleware(self._environ, Mock())
        
        route_handler = self._environ.get("route_/simple/request_handler")
        
        self.assertIsNotNone(route_handler)
        self.assertIsInstance(route_handler.get("controller"), SimpleController)
        self.assertEqual("do_request", route_handler.get("method"))
        
    def test_route_norequest_built(self):
        '''This test case ensures an exception is raised if no request is available in wsgi environ.'''
        
        self.assertRaises(FantasticoNoRequestError, self._routing_middleware, *[self._environ, Mock()])
        
    def test_route_unhandled_exception(self):
        '''This test case ensures that unhandled exceptions are correctly transformed to fantastico exceptions.'''
        
        self._environ["fantastico.request"] = Request.blank("/simple/request")
        
        self._router.handle_route = Mock(side_effect=Exception("Unhandled error"))
        
        with self.assertRaises(FantasticoError) as cm:
            self._routing_middleware(self._environ, Mock())
        
        self.assertTrue(str(cm.exception).find("Unhandled error") > -1)
        
    def test_router_registration_ok(self):
        '''This test case ensures that routing middleware correctly calls underlining methods from the given router
        so that it correctly discovers all available routes.'''
        
        self.get_loaders_invoked = False
        self.register_routes_invoked = False
        
        def get_loaders():
            self.get_loaders_invoked = True
            
        def register_routes():
            self.register_routes_invoked = True
        
        router = Mock()
        router_cls = Mock(return_value=router)
        router.get_loaders = lambda: get_loaders()
        router.register_routes = lambda: register_routes()
        
        RoutingMiddleware(Mock(), router_cls)
        
        self.assertTrue(self.get_loaders_invoked)
        self.assertTrue(self.register_routes_invoked)
        
class SimpleController(object):
    '''Class used to simulate a controller that can handle certain requests.'''
     
    pass