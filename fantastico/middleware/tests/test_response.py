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
from webob.response import Response
import unittest

class ResponseTests(unittest.TestCase):
    '''Class used to provide the test cases that ensure response object is correctly provided for future use.'''
    
    def test_case_response_ok(self):
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