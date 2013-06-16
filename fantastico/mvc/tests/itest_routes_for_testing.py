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
.. py:module:: fantastico.mvc.tests.itest_routes_for_testing
'''
from fantastico.exceptions import FantasticoTemplateNotFoundError
from fantastico.mvc.tests.routes_for_testing import RoutesForControllerTesting
from fantastico.mvc.tests.subroutes.subroutes_controller import SubroutesController
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from mock import Mock

class RoutesForTestingIntegration(FantasticoIntegrationTestCase):
    '''This test suite check that routes for testing correctly works.'''
    
    def test_say_hello_ok(self):
        '''This test case ensure response is retrieved correctly from say hello.'''
        
        def exec_test(env, settings_cls):
            controller = RoutesForControllerTesting(SettingsFacade())
            response = controller.say_hello(Mock())
            
            self.assertIsNotNone(response)
            self.assertTrue(response.text.find("Hello world.") > -1)
            
        self._run_test_all_envs(exec_test)
        
    def test_upload_file_ok(self):
        '''This test case ensure response is retrieved correctly from upload file.'''
        
        def exec_test(env, settings_cls):
            controller = RoutesForControllerTesting(SettingsFacade())
            response = controller.upload_file(Mock())
            
            self.assertIsNotNone(response)
            self.assertTrue(response.text.find("Hello world.") > -1)
            
        self._run_test_all_envs(exec_test)
        
    def test_subroute_ok(self):
        '''This test case ensure method is correctly executed from SubroutesController.'''
        
        def exec_test(env, settings_cls):
            controller = SubroutesController(SettingsFacade())
            self.assertRaises(FantasticoTemplateNotFoundError, controller.handle_route, *[Mock()])
            
        self._run_test_all_envs(exec_test)