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
.. py:module:: fantastico.server.tests.itest_dev_server
'''
from fantastico.routing_engine.dummy_routeloader import DummyRouteLoader
from fantastico.server.dev_server import DevServer
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from urllib.error import HTTPError
from urllib.request import Request
import threading
import time
import urllib

class DevServerIntegration(FantasticoIntegrationTestCase):
    '''This class provides the test cases for making sure dev server component works as expected.'''
    
    def test_server_runs_ok(self):
        '''This test case makes sure dev server can start correctly. In addition it requests dummy route test page
        and assert for the result.'''
        
        server = DevServer()
        
        def start_server():
            server.start()
            
        def stop_server():
            try:
                while not server.started:
                    time.sleep(0.01)
                    
                self.assertTrue(server.started)
                
                url = "http://localhost:12000%s" % DummyRouteLoader.DUMMY_ROUTE
                request = Request(url) 
                with self.assertRaises(HTTPError) as cm:
                    urllib.request.urlopen(request)
                    
                self.assertEqual(400, cm.exception.code)
                self.assertEqual("Hello world.", cm.exception.read().decode())
            finally:
                server.stop()
        
        thread_start = threading.Thread(target=start_server)
        thread_start.start()
        
        thread_stop = threading.Thread(target=stop_server)
        thread_stop.start()
                
        thread_stop.join()
        
        self.assertEqual(12000, server.port)
        self.assertEqual("localhost", server.hostname)