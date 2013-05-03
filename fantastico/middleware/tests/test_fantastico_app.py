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
.. py:module:: fantastico.middleware.tests.fantastico_app
'''
from fantastico.exceptions import FantasticoClassNotFoundError, \
    FantasticoContentTypeError, FantasticoNoRequestError,\
    FantasticoRouteNotFoundError
from fantastico.middleware.fantastico_app import FantasticoApp
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from webob.request import Request
from webob.response import Response

class FantasticoAppTests(FantasticoUnitTestsCase):
    '''Class that provides the test suite for ensuring that fantastico wsgi app is working as expected.'''

    def init(self):
        self._old_call = FantasticoApp.__call__
        
        self._settings_facade = Mock()
        self._settings_facade_cls = Mock(return_value=self._settings_facade)
        
        self._request = Request.blank("/simple/request")
        self._request.content_type = "text/html"
        self._controller = Mock()
        self._controller.exec_logic = Mock(return_value=Response(content_type="text/html"))
        self._environ = {"fantastico.request": self._request, 
                         "route_/simple/request_handler": {"controller": self._controller,
                                                           "method": "exec_logic"}}
 
    def cleanup(self):
        FantasticoApp.__call__ = self._old_call
        
    def test_middlewares_wrapped(self):
        '''Test case that ensures configured middlewares from a config profile are wrapped in the correct order.'''
        
        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware"])
        
        app = FantasticoApp(self._settings_facade_cls)        
        
        app(self._environ, Mock())

        self.assertTrue(self._environ.get("test_wrapped_ok"))
        
        chained_resp = self._environ.get("middlewares_responses")
        self.assertIsNotNone(chained_resp)
        self.assertEqual(1, len(chained_resp))
        self.assertEqual(["middleware"], chained_resp)
        
        
    def test_middleware_wrapped_in_order(self):
        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware",
                                                       "fantastico.middleware.tests.test_fantastico_app.MockedMiddleware2",
                                                       "fantastico.middleware.tests.test_fantastico_app.MockedMiddleware3"])
        
        app = FantasticoApp(self._settings_facade_cls)

        app(self._environ, Mock())
        
        self.assertTrue(self._environ.get("test_wrapped_ok"))
        
        chained_resp = self._environ.get("middlewares_responses")
        self.assertIsNotNone(chained_resp)
        self.assertEqual(3, len(chained_resp))
        self.assertEqual(["middleware", "middleware2", "middleware3"], chained_resp)
        
    def test_wrap_no_middleware(self):
        '''Test case that ensures the app entry point works as expected even if no middlewares are installed.'''
        
        self._settings_facade.get = Mock(return_value=[])
        
        app = FantasticoApp(self._settings_facade_cls)

        app(self._environ, Mock())
        
        self.assertTrue(True)
        
    def test_middleware_not_found_ex(self):
        '''Test case that ensures an exception is raised when an invalid middleware is specified.'''
        
        self._settings_facade.get = Mock(return_value=["not.found.exception"])        
        self.assertRaises(FantasticoClassNotFoundError, FantasticoApp, *[self._settings_facade_cls])
        
        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware1099"])
        self.assertRaises(FantasticoClassNotFoundError, FantasticoApp, *[self._settings_facade_cls])
        
    def test_exec_controller_ok(self):
        '''This test case ensures that requested route is executed - success scenario.'''

        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware"])        
                
        app_middleware = FantasticoApp(self._settings_facade_cls)
        
        response = Response()
        response.content_type = "text/html"
        response.text = "Hello world"
        
        self._controller.exec_logic = lambda request: response
        
        self.assertEqual([b"Hello world"], app_middleware(self._environ, Mock()))
        self.assertTrue(self._environ["test_wrapped_ok"])
    
    def test_missing_request(self):
        '''This test case ensures an exception is raised if request middleware was not executed correctly.'''

        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware"])        
                
        app_middleware = FantasticoApp(self._settings_facade_cls)
        
        del self._environ["fantastico.request"]
        self.assertRaises(FantasticoNoRequestError, app_middleware, *[self._environ, Mock()])
        
        self._environ["fantastico.request"] = None
        self.assertRaises(FantasticoNoRequestError, app_middleware, *[self._environ, Mock()])
        
    def test_route_notfound(self):
        '''This test case ensures an exception is raised whenever the route requested can not be find.'''
        
        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware"])        
                
        app_middleware = FantasticoApp(self._settings_facade_cls)

        del self._environ["route_/simple/request_handler"]
        self.assertRaises(FantasticoRouteNotFoundError, app_middleware, *[self._environ, Mock()])
        
        self._environ["route_/simple/request_handler"] = None
        self.assertRaises(FantasticoRouteNotFoundError, app_middleware, *[self._environ, Mock()])
    
    def test_route_nomethod(self):
        '''This test case ensures an exception is raised whenever route method is not set correctly.'''
        
        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware"])        
                
        app_middleware = FantasticoApp(self._settings_facade_cls)
        
        route_handler = "route_/simple/request_handler" 
        
        del self._environ[route_handler]["method"]        
        self.assertRaises(FantasticoRouteNotFoundError, app_middleware, *[self._environ, Mock()])
        
        self._environ[route_handler]["method"] = None
        self.assertRaises(FantasticoRouteNotFoundError, app_middleware, *[self._environ, Mock()])

        self._environ[route_handler]["method"] = ""
        self.assertRaises(FantasticoRouteNotFoundError, app_middleware, *[self._environ, Mock()])
        
    def test_route_nocontroller(self):
        '''This test case ensures an exception is raised whenever route controller is not set correctly.'''

        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware"])        
                
        app_middleware = FantasticoApp(self._settings_facade_cls)
        
        route_handler = "route_/simple/request_handler" 
        
        del self._environ[route_handler]["controller"]
        self.assertRaises(FantasticoRouteNotFoundError, app_middleware, *[self._environ, Mock()])        

        self._environ[route_handler]["controller"] = None
        self.assertRaises(FantasticoRouteNotFoundError, app_middleware, *[self._environ, Mock()])        
        
    def test_mistmatch_content_headers(self):
        '''This test case makes sure an exception is raised whenever request content type is different than response
        content type.'''
        
        self._settings_facade.get = Mock(return_value=["fantastico.middleware.tests.test_fantastico_app.MockedMiddleware"])        

        response = Response()
        response.content_type = "application/json"
        response.text = "Hello world"
        
        self._controller.exec_logic = lambda request: response
        
        app_middleware = FantasticoApp(self._settings_facade_cls)
        
        self.assertRaises(FantasticoContentTypeError, app_middleware, *[self._environ, Mock()])            
        self.assertTrue(self._environ["test_wrapped_ok"])
        
class MockedMiddleware(object):
    '''This is a mocked middleware used for unit testing purposes.'''
    
    def __init__(self, app):
        self._app = app
        
    def __call__(self, environ, start_response):
        '''Method used to provide a very simple middleware action which can be asserted against.'''
        
        environ["test_wrapped_ok"] = True
        
        tmp = environ.get("middlewares_responses", [])
        tmp.append("middleware")
        environ["middlewares_responses"] = tmp
        
        return self._app(environ, start_response)
    
class MockedMiddleware2(object):
    '''This is a mocked middleware used for unit testing purposes.'''
    
    def __init__(self, app):
        self._app = app
        
    def __call__(self, environ, start_response):
        '''Method used to provide a very simple middleware action which can be asserted against.'''
        
        environ["middlewares_responses"].append("middleware2")
        
        return self._app(environ, start_response)
    
class MockedMiddleware3(object):
    '''This is a mocked middleware used for unit testing purposes.'''
    
    def __init__(self, app):
        self._app = app
        
    def __call__(self, environ, start_response):
        '''Method used to provide a very simple middleware action which can be asserted against.'''
        
        environ["middlewares_responses"].append("middleware3")
        
        return self._app(environ, start_response)