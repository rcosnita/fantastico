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
.. py:module:: fantastico.mvc.tests.routes_for_testing
'''
from fantastico.mvc.controller_decorators import Controller, ControllerProvider
from webob.response import Response

@ControllerProvider()
class RoutesForControllerTesting(object):
    '''This class defines two methods as Controllers.'''
    
    @Controller(url="/say_hello", method="GET")
    def say_hello(self, request):
        response = Response()
        response.text = "Hello world."
        
        return response
    
    @Controller(url="/upload_file", method=["POST"], models={"File": "fantastico.filesystem.models.File"})
    def upload_file(self, request):
        response = Response()
        response.text = "Hello world."
        
        return response