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

class FantasticoAppIntegration(FantasticoIntegrationTestCase):
    '''Class used to make sure fantastico can correctly handle requests.'''
    
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

        self._middleware = FantasticoApp()
        
    def test_request_ok(self):
        '''Test case than ensures requests are handled correctly by fantastico app (all configured middlewares are doing)
        what they are supposed to do.'''
        
        self._middleware(self._environ, Mock())
        
        request = self._environ.get("fantastico.request")
        
        self.assertIsNotNone(request)