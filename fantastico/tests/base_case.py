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

.. py:module:: fantastico.tests.base_case
'''
from fantastico.settings import BasicSettings
import os
import unittest

class FantasticoBaseTestCase(unittest.TestCase):
    '''This is the base class that must be inherited by each specific test case: Unit tests / Integration tests'''
    
    def setUp(self):
        '''We make the convention that setup method will always invoke init method for each test case.'''
        
        if hasattr(self, "init"):
            init = getattr(self, "init")
            init()
    
class FantasticoUnitTestsCase(FantasticoBaseTestCase):
    '''This is the base class that must be inherited by each unit test written for fantastico.
    
    .. code-block:: python
    
        class SimpleUnitTest(FantasticoUnitTestsCase):
            def init(self):
                self._msg = "Hello world"
                
            def test_simple_flow_ok(self):
                self.assertEqual("Hello world", self._msg)'''
    
    def setUp(self):
        super(FantasticoUnitTestsCase, self).setUp()
    
class FantasticoIntegrationTestCase(FantasticoBaseTestCase):
    '''This is the base class that must be inherited by each integration test written for fantastico.

    .. code-block:: python
    
        class SimpleIntegration(FantasticoIntegrationTestCase):
            def init(self):
                self.simple_class = {}
                
            def test_simple_ok(self):
                def do_stuff(env, env_cls):
                    self.assertEqual(simple_class[env], env_cls)
                    
                self._run_test_all_envs(do_stuff)
    '''
    
    @property
    def _envs(self):
        '''Private property that holds the environments against which we run the integration tests.'''
        
        return self.__envs
    
    def setUp(self):
        self.__envs = [("fantastico.settings.BasicSettings", BasicSettings)]
        
        super(FantasticoIntegrationTestCase, self).setUp()
        
    def _run_test_all_envs(self, callableObj):
        '''This method is used to execute a callable block of code on all environments. This is extremely useful for
        avoid boiler plate code duplication and executing test logic against all environments.        
        '''
        
        old_env = os.environ.get("FANTASTICO_ACTIVE_CONFIG")
        
        for env, settings_cls in self._envs:
            try:
                os.environ["FANTASTICO_ACTIVE_CONFIG"] = env
                
                callableObj(env, settings_cls)
            finally:
                if old_env is None:
                    old_env = ""
                    
                os.environ["FANTASTICO_ACTIVE_CONFIG"] = old_env