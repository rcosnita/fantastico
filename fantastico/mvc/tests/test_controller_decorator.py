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
.. py:module:: fantastico.mvc.tests.test_controller_decorator
'''
from fantastico.mvc.controller_decorators import Controller
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from webob.response import Response

class ControllerDecoratorTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for controller decorator.'''
    
    def test_controller_registration_ok(self):
        '''This test case checks that routes are correctly registered by controller decorator.'''
        
        from fantastico.mvc.tests.routes_for_testing import RoutesForControllerTesting
        
        registered_routes = Controller.get_registered_routes()
        
        hello_route = registered_routes.get("/say_hello")

        self.assertIsNotNone(hello_route)
        self.assertIsInstance(hello_route, Controller)
        self.assertEqual("/say_hello", hello_route.url)
        self.assertEqual(["GET"], hello_route.method)
        self.assertEqual({}, hello_route.models)
        self.assertEqual(RoutesForControllerTesting.say_hello, hello_route.fn_handler)
        
        response = hello_route.fn_handler(RoutesForControllerTesting(), Mock())
        self.assertIsInstance(response, Response)
        self.assertEqual(b"Hello world.", response.body)
        
    def test_controller_list_params_ok(self):
        '''This test case checks list parameters of controller (models, method) work as expected.'''

        from fantastico.mvc.tests.routes_for_testing import RoutesForControllerTesting

        registered_routes = Controller.get_registered_routes()
        
        upload_file = registered_routes.get("/upload_file")

        self.assertIsNotNone(upload_file)
        self.assertIsInstance(upload_file, Controller)
        self.assertEqual("/upload_file", upload_file.url)
        self.assertEqual(["POST"], upload_file.method)
        self.assertEqual({"File": "fantastico.filesystem.models.File"}, upload_file.models)
        self.assertEqual(RoutesForControllerTesting.upload_file, upload_file.fn_handler)
        
        response = upload_file.fn_handler(RoutesForControllerTesting(), Mock())
        self.assertIsInstance(response, Response)
        self.assertEqual(b"Hello world.", response.body)