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
from fantastico.exceptions import FantasticoClassNotFoundError, FantasticoControllerInvalidError
from fantastico.mvc import controller_decorators
from fantastico.tests.base_case import FantasticoUnitTestsCase, FakeControllerDecorator
from mock import Mock
from webob.response import Response

class Model1(object):
    pass

class Model2(object):
    pass

class ControllerDecoratorTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for controller decorator.'''
    
    @classmethod
    def setup_once(cls):
        '''We rebind original Controller decorator to its module.'''
        
        super(ControllerDecoratorTests, cls).setup_once()
         
        controller_decorators.Controller = cls._old_controller_decorator
    
    def test_controller_registration_ok(self):
        '''This test case checks that routes are correctly registered by controller decorator.'''
        
        from fantastico.mvc.tests.routes_for_testing import RoutesForControllerTesting
        
        registered_routes = controller_decorators.Controller.get_registered_routes()
        
        hello_route = registered_routes.get("/say_hello")

        self.assertIsNotNone(hello_route)
        self.assertIsInstance(hello_route, controller_decorators.Controller)
        self.assertEqual("/say_hello", hello_route.url)
        self.assertEqual(["GET"], hello_route.method)
        self.assertEqual({}, hello_route.models)
        self.assertEqual("fantastico.mvc.tests.routes_for_testing.RoutesForControllerTesting.say_hello",
                         hello_route.fn_handler.full_name)
        
        response = hello_route.fn_handler(RoutesForControllerTesting(settings_facade=Mock()), Mock())
        self.assertIsInstance(response, Response)
        self.assertEqual(b"Hello world.", response.body)
        
    def test_controller_list_params_ok(self):
        '''This test case checks list parameters of controller (models, method) work as expected.'''

        from fantastico.mvc.tests.routes_for_testing import RoutesForControllerTesting

        registered_routes = controller_decorators.Controller.get_registered_routes()
        
        upload_file = registered_routes.get("/upload_file")

        self.assertIsNotNone(upload_file)
        self.assertIsInstance(upload_file, controller_decorators.Controller)
        self.assertEqual("/upload_file", upload_file.url)
        self.assertEqual(["POST"], upload_file.method)
        self.assertEqual({"File": "fantastico.mvc.tests.routes_for_testing.File"}, upload_file.models)
        self.assertEqual("fantastico.mvc.tests.routes_for_testing.RoutesForControllerTesting.upload_file",
                         upload_file.fn_handler.full_name)
        
        response = upload_file.fn_handler(RoutesForControllerTesting(settings_facade=Mock()), Mock())
        self.assertIsInstance(response, Response)
        self.assertEqual(b"Hello world.", response.body)
    
    def test_controller_model_injection(self):
        '''This test case ensures models required by controllers are correctly injected.'''
        
        class FakeFacade(object):
            def __init__(self, model_cls, session):
                self.model_cls = model_cls
                self._session = session
                    
        @controller_decorators.Controller(url="/simple/controller", method="GET",
            models={"Model1": "fantastico.mvc.tests.test_controller_decorator.Model1",
                    "Model2": "fantastico.mvc.tests.test_controller_decorator.Model2"},
            model_facade=FakeFacade)
        def do_stuff(request):
            '''This method does nothing. We only check request model injection algorithm.'''
        
            pass

        request = Mock()
        request.models = None
        
        self.assertIsNone(do_stuff(request))
        self.assertIsNotNone(request.models)
        self.assertEqual(request.models.Model1.model_cls, Model1)
        self.assertEqual(request.models.Model2.model_cls, Model2)
        self.assertIsNone(request.models.NotFoundModel)
    
    def test_controller_model_injection_clsnotfound(self):
        '''This test case ensures a fantastico exception is raised when a model is not found.'''
        
        @controller_decorators.Controller(url="/simple/controller", method="GET",
                    models={"Model1": "fantastico.mvc.tests.test_controller_decorator.ModelNotFound"})
        def do_stuff(request):
            pass
        
        with self.assertRaises(FantasticoClassNotFoundError):
            do_stuff(Mock())
    
    def test_controller_wrongly_defined(self):
        '''This test case ensures a fantastico exception is raised when a controller method does not have
        a request parameter.'''
        
        @controller_decorators.Controller(url="/simple/controller", method="GET")
        def do_stuff():
            pass
        
        with self.assertRaises(FantasticoControllerInvalidError):
            do_stuff()