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

.. py:module:: fantastico.middleware.tests.test_response
'''
from fantastico.tests.base_case import FantasticoUnitTestsCase
from webob.response import Response


class ResponseTests(FantasticoUnitTestsCase):
    '''Class used to provide the test cases that ensure response object is correctly provided for future use.'''
    
    def test_response_ok(self):
        '''Test case that ensures response object behaves as expected. If this pass it guarantees webob version does not
        break fantastico functionality.'''
        
        response = Response()
        
        self.assertEqual(200, response.status_code)
        self.assertEqual("text/html", response.content_type)
        
        response.charset = "utf8"
        self.assertEqual("utf8", response.charset)
        
        response.text = "test content"
        self.assertEqual(b"test content", response.body)

        response.body = b"test content"
        self.assertEqual(b"test content", response.body)
        
        response.status = 404
        self.assertEqual(404, response.status_code)
        
        response.content_type = "application/json"
        self.assertEqual("application/json", response.content_type)
        
    def test_response_headers_ok(self):
        '''Test case that ensures headers can be correctly set to a response instance.'''
        
        response = Response()
        
        response.headers.add("BEARER_TOKEN", "12345")
        
        self.assertEqual("12345", response.headers.get("BEARER_TOKEN"))
        
    def test_response_cookie_ok(self):
        '''Test case that ensures cookies can be correctly set to a response instance.'''
        
        response = Response()
        
        response.set_cookie("fantastico.sid", "12345", max_age=360, path="/", secure=True)
        
        cookie = response.headers["Set-Cookie"]
        
        self.assertGreater(cookie.find("fantastico.sid=12345"), -1)
        self.assertGreater(cookie.find("Max-Age=360"), -1)
        self.assertGreater(cookie.find("secure"), -1)
        self.assertGreater(cookie.find("Path=/"), -1)