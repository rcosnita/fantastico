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

.. py:module:: fantastico.middleware.tests.itest_request_middleware
'''
from fantastico.middleware.request_middleware import RequestMiddleware
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from mock import Mock
from fantastico.routing_engine.custom_responses import RedirectResponse

class RequestMiddlewareIntegration(FantasticoIntegrationTestCase):
    '''Test suite that ensures requqest middleware is working properly into it's native running environment (no mocked essential
    dependencies). It ensures integration all available environments configuration.'''
    
    def init(self):        
        self._environ = {"CONTENT_TYPE": "application/json",
                           "HTTP_ACCEPT": "application/json",
                           "HTTP_ACCEPT_LANGUAGE": "ro-ro,en-US;q=0.8",
                           "HTTP_OAUTH_BEARER": "123",
                           "HTTP_HOST": "localhost:80",
                           "PATH_INFO": "/article",
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
        
        self._middleware = RequestMiddleware(Mock())

    def test_context_initialization(self):
        '''Test case that ensures context is correctly initialized.'''
        
        def exec_test(env, settings_cls):
            self._middleware(self._environ, Mock())
            
            request = self._environ.get("fantastico.request")
            
            self.assertIsNotNone(request)
            self.assertIsNotNone(request.request_id)
            self.assertEqual("GET", request.method)
            self.assertEqual("application/json", request.content_type)
            self.assertEqual("123", request.headers.get("oauth_bearer"))
            self.assertEqual(1, int(request.params.get("id")))
            
            self.assertEqual(settings_cls().installed_middleware, request.context.settings.get("installed_middleware"))
            self.assertEqual(settings_cls().supported_languages, request.context.settings.get("supported_languages"))
            
            self.assertEqual("en_us", request.context.language.code)
        
        self._run_test_all_envs(exec_test)
    
    def test_redirect_ok(self):
        '''This test case ensures request redirection works as expected.'''
        
        def exec_test(env, settings_cls):
            self._middleware(self._environ, Mock())
            
            request = self._environ.get("fantastico.request")
            
            self.assertIsNotNone(request)
            
            response = request.redirect("/test/url", [("p1", "hello"), ("p2", "world")])
            
            self.assertIsNotNone(response)
            self.assertIsInstance(response, RedirectResponse)
            self.assertEqual(301, response.status_code)
            self.assertEqual("/test/url?p1=hello&p2=world", response.headers["Location"])
        
        self._run_test_all_envs(exec_test)