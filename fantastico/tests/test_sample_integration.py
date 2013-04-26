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

.. py:module:: fantastico.tests.test_sample
'''
from fantastico.settings import BasicSettings
from fantastico.tests.base_case import FantasticoIntegrationTestCase

class BaseTestingHierarchyTest(FantasticoIntegrationTestCase):
    '''Test case that ensures fantastico integration base class is working properly.'''
    
    def init(self):
        self._additional_parameter = "test param"
                
    def test_execution_on(self):
        self._basic_settings = False
                
        def execute_test(env, settings_cls):
            if settings_cls == BasicSettings:
                self._basic_settings_ok = True
                
            self.assertEqual("test param", self._additional_parameter)
            
        self._run_test_all_envs(execute_test)
        
        self.assertTrue(self._basic_settings_ok)