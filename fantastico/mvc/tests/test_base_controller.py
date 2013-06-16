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

.. py:module:: fantastico.mvc.tests.test_base_controller
'''
from fantastico.exceptions import FantasticoTemplateNotFoundError, FantasticoError
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc import controller_decorators
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from webob.response import Response

NewControllerTesting = None

class BaseControllerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for base controller class.'''
    
    @classmethod
    def setup_once(cls):
        '''We rebind original Controller decorator to its module.'''
        
        super(BaseControllerTests, cls).setup_once()
         
        controller_decorators.Controller = cls._old_controller_decorator
        
        @controller_decorators.ControllerProvider()
        class NewControllerTestingNested(BaseController):
            '''This is just a simple controller used for testing purposes.'''
            
            @controller_decorators.Controller(url="/unit/tests/base/say-hello", method="GET", conn_manager=Mock())
            def say_hello(self, request):
                tpl = self.load_template("/say_hello.html")
                
                response = Response(tpl)
                response.content_type = "text/html"
                
                return response
        
        global NewControllerTesting
        
        NewControllerTesting = NewControllerTestingNested
        
    def init(self):
        self._settings_facade = Mock()
        self._settings_facade.get_root_folder = Mock(return_value=self._get_root_folder())
                
    def test_get_component_folder(self):
        '''This test case ensure component folder is detected correctly.'''
        
        controller = BaseController(self._settings_facade)
        
        component_name = controller.get_component_folder()
        
        self.assertEqual("fantastico/mvc", component_name)
        
    def test_get_component_folder_for_children(self):
        '''This test case ensures component folder is correctly detected for children.'''

        controller = NewControllerTesting(self._settings_facade)
        
        component_name = controller.get_component_folder()
        
        self.assertEqual("fantastico/mvc/tests", component_name)
        
    def test_load_template_correctly(self):
        '''This test case ensures a controller can correctly loads a template using jinja2.'''

        with open(self._get_root_folder() + "fantastico/mvc/tests/views/say_hello.html", "r") as template:
            expected_response = template.read()

        self._settings_facade.get = Mock(return_value={})
        controller = NewControllerTesting(self._settings_facade)
        
        response = controller.say_hello(Mock())
        
        self.assertIsInstance(response, Response)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.body)
        self.assertEqual(expected_response, response.body.decode())
        
    def test_load_template_notfound(self):
        '''This test case ensures that a specific exception is raised when template is not found.'''
        
        self._settings_facade.get = Mock(return_value={})
        
        controller = NewControllerTesting(self._settings_facade)
        self.assertRaises(FantasticoTemplateNotFoundError, controller.load_template, *["no_fun.html"])
        
    def test_load_template_unexpected_exception(self):
        '''This test case ensures that an unexpected exception raised during loading a template is casted to
        a :py:class:`fantastico.exceptions.FantasticoError`.'''
        
        self._settings_facade.get = Mock(return_value={})
        get_template = Mock(side_effect=Exception("Unexpected error"))
        
        controller = NewControllerTesting(self._settings_facade)
        with self.assertRaises(FantasticoError) as cm:
            controller.load_template("no_fun", get_template=get_template)
            
        self.assertTrue(str(cm.exception).find("Unexpected error") > -1)