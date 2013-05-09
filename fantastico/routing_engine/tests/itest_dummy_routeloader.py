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
.. py:module:: fantastico.routing_engine.tests.itest_dummy_routeloader
'''

from fantastico.routing_engine.dummy_routeloader import DummyRouteLoader
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from urllib.error import HTTPError
from urllib.request import Request
import urllib

class DummyRouteLoaderIntegration(DevServerIntegration):
    '''This class provides the test suite for ensuring dummy route provided by dummy route loader is correctly registered.'''
    
    def init(self):
        self._exception = None
    
    def test_server_runs_ok(self):
        '''This test case makes sure dev server can start correctly. In addition it requests dummy route test page
        and assert for the result.'''
        
        def request_logic(server):
            request = Request(self._get_server_base_url(server, DummyRouteLoader.DUMMY_ROUTE)) 
            with self.assertRaises(HTTPError) as cm:
                urllib.request.urlopen(request)
            
            self._exception = cm.exception
            
        def assert_logic(server):
            self.assertEqual(400, self._exception.code)
            self.assertTrue(self._exception.read().decode().find("Hello world.") > -1)            
            
        self._run_test_all_envs(lambda env, settings_cls: self._run_test_against_dev_server(request_logic, assert_logic))
        
    def test_http_verb_incompatible(self):
        '''This test case guarantees that a route can not be invoked with the wrong http verb.'''
        
        def request_logic(server):
            request = Request(self._get_server_base_url(server, DummyRouteLoader.DUMMY_ROUTE))
             
            data = {"username": "radu"}
            data = urllib.parse.urlencode(data).encode()
            
            with self.assertRaises(HTTPError) as cm:
                urllib.request.urlopen(request, data)
            
            self._exception = cm.exception
            
        def assert_logic(server):
            self.assertEqual(500, self._exception.code)
            
        self._run_test_all_envs(lambda env, settings_cls: self._run_test_against_dev_server(request_logic, assert_logic))