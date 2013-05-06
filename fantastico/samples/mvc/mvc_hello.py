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
.. py:module:: fantastico.samples.mvc.mvc_hello
'''
from fantastico.mvc.controller_decorators import Controller, ControllerProvider
from fantastico.settings import SettingsFacade
from webob.response import Response

@ControllerProvider()
class MvcHelloController(object):
    '''This class provides some simple examples of how to write controllers based on Fantastico mvc.'''
    
    def __init__(self, settings_facade=SettingsFacade):
        self._settings_facade = settings_facade
    
    @Controller(url="/mvc/hello-world", method="GET")
    def say_hello(self, request):
        response = Response(content_type=request.content_type)
        
        response.text = "<h1>Hello world. It works like a charm.</h1>"
        
        return response