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

.. py:module:: fantastico.routing_engine.tests.itest_router
'''
from fantastico.routing_engine.router import Router
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from fantastico.exceptions import FantasticoRouteNotFoundError

class RouterIntegration(FantasticoIntegrationTestCase):
    '''This class provides all test cases to ensure router is correctly working in all available configuration profiles.'''
    
    def init(self):
        self._environ = {}
        
    def test_route_not_found(self):
        '''Test case that ensures an exception is raised when a page is not found.'''
        
        def exec_logic(env, settings_cls):
            self._router = Router(settings_cls)
            
            self.assertRaises(FantasticoRouteNotFoundError, self._router.handle_route,
                              *["/sure/url/not/found/in/here", self._environ])
            
        self._run_test_all_envs(exec_logic)