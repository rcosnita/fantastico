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

.. py:module:: fantastico.middleware.tests.test_request_middleware
'''
from fantastico.middleware.request_response import RequestResponseMiddleware
from mock import Mock
from unittest.case import TestCase

class RequestMiddlewareTests(TestCase):
    '''Test suite for ensuring that environ wsgi dictionary is correctly converted to a request object.'''
    
    def setUp(self):
        self._app = Mock()
        self._start_response = Mock()
        self._middleware = RequestResponseMiddleware(self._app)
    
    def test_convert_request_ok(self):
        '''Test case that ensuring that request conversion works as expected.'''
        
        environ = {"ACCEPT": "application/json",
                   "CONTENT_TYPE": "application/json",
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
        
        self._middleware(environ, self._start_response)
        
        request = environ.get("fantastico.request")
        
        self.assertIsNotNone(request)
        self.assertEqual("GET", request.method)
        self.assertEqual("http", request.scheme)
        self.assertEqual("", request.script_name)
        self.assertEqual("/article", request.path_info)
        self.assertEqual("localhost:80", request.host)
        self.assertTrue("application/json" in request.accept)
        self.assertEqual("application/json", request.content_type)
        self.assertEqual("123", request.headers.get("oauth_bearer"))
        self.assertEqual(1, int(request.params.get("id")))        
        
        